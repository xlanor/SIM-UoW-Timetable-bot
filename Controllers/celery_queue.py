#! /usr/bin/env python3
# -*- coding: utf-8 -*-
##
#   Copyright (C) 2018 JING KAI TAN
#
#   This program is free software: you can redistribute it and/or modify it
#   under the terms of the GNU Affero General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or (at your
#   option) any later version.
#
#   This program is distributed in the hope that it will be useful, but WITHOUT
#   ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
#   FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Affero General Public
#   License for more details.
#
#   You should have received a copy of the GNU Affero General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##
#  Methods for the registration process.
##
# Celery functions.
##
from typing import Dict
from typing import List
import traceback
import jsonpickle
import arrow

# Local Imports
from Controllers.Ripper.ripper import RipperFactory
import Controllers.db_facade as dbInterface
from Models.exceptions import *
from Models.user_object import UserObject
from celery import Celery
from cel import app
from Models.encryption import Encrypt
from cfg import Configuration


@app.task
def register_user(user_data: Dict, bot):
    config = Configuration()
    r = config.REDIS_INSTANCE
    user_id = user_data["user_id"]
    try:
        bot = jsonpickle.decode(bot)

        username = user_data["username"]
        password = user_data["password"]
        name = user_data["name"]
        user_input_application_key = user_data["application_key"]
        encrypted_password = Encrypt(
            user_data["password"], user_input_application_key
        ).encrypt()
        try:
            timetable_result = get_timetable(username, password, user_id, bot)
            print(f"Classes retrieved: {len(timetable_result)}")
            # Now, let us begin constructing our database insertion object.
            obj_to_insert = UserObject(user_id, username, name, encrypted_password)
            obj_to_insert.add_classes(timetable_result)
            dbInterface.insert_new_user(obj_to_insert)
            success_message = [
                f"A total of {obj_to_insert.get_class_leng()} records have been synced to the database\n"
            ]
            success_message.append(
                "You can now use /timetable to retrieve your timetable\n"
            )
            success_message.append(
                "In addition, please take note of the following handlers:\n"
            )
            success_message.append(
                "```Daily reminder at 7am in the morning - /alert ```\n"
            )
            success_message.append(
                "```Nightly reminder at 10pm at night - /nightly ```\n"
            )

            success_message.append("Both of these handlers act as a toggle.")
            message = "".join(success_message)
            r.delete(user_id)
            bot.send_message(chat_id=user_id, text=message, parse_mode="Markdown")

        except UnableToLogin:
            # Unable to login with given credentials.
            # new_ripper attempts to login and raises an UnableToLogin exception
            # if it cant be logged in.
            error_message = ["Unable to login with your credentials!\n"]
            error_message.append("Please try to register again using /register")
            err = "".join(error_message)
            r.delete(user_id)
            bot.send_message(chat_id=user_id, text=err, parse_mode="Markdown")
    except Exception as e:
        # to send to github
        local = arrow.utcnow().to("Asia/Singapore")
        local_time = local.format("YYYY-MM-DD HH:mm:ss ZZ")
        bot.send_message(
            chat_id=config.ERROR_CHANNEL, text=f"An error occured at {local_time}"
        )
        bot.send_message(
            chat_id=config.ERROR_CHANNEL,
            text=f"The error was: {traceback.format_exc()}",
        )
        bot.send_message(
            chat_id=config.ERROR_CHANNEL,
            text=f"This message was triggered in celery. User data: {str(user_data)}",
        )
        r.delete(user_id)
        pass


@app.task
def update_user(telegram_id: str, user_name: str, password: str, bot):

    config = Configuration()
    r = config.REDIS_INSTANCE
    bot = jsonpickle.decode(bot)
    try:

        list_of_classes = get_timetable(user_name, password, telegram_id, bot)
        dbInterface.update_classes(list_of_classes, telegram_id)
        message = (
            f"A total of *{len(list_of_classes)}* records were resynced to the database"
        )
        r.delete(telegram_id)
        bot.send_message(chat_id=telegram_id, text=message, parse_mode="Markdown")
    except UnableToLogin:
        # Unable to login with given credentials.
        # new_ripper attempts to login and raises an UnableToLogin exception
        # if it cant be logged in.
        error_message = ["Unable to login with your credentials!\n"]
        error_message.append(
            "Please try to wipe your details and register again using /register"
        )
        err = "".join(error_message)
        r.delete(telegram_id)
        bot.send_message(chat_id=telegram_id, text=err, parse_mode="Markdown")
    except Exception as e:
        local = arrow.utcnow().to("Asia/Singapore")
        local_time = local.format("YYYY-MM-DD HH:mm:ss ZZ")
        bot.send_message(
            chat_id=config.ERROR_CHANNEL, text=f"An error occured at {local_time}"
        )
        bot.send_message(
            chat_id=config.ERROR_CHANNEL,
            text=f"The error was: {traceback.format_exc()}",
        )
        bot.send_message(
            chat_id=config.ERROR_CHANNEL,
            text=f"This message was triggered in celery. Triggered by: {telegram_id}",
        )
        r.delete(telegram_id)
        pass


def get_timetable(username: str, password: str, user_id: str, bot) -> List:
    # Able to login with given credentials.
    timetable_ripper = RipperFactory.get_ripper("NewRip", username, password)
    timetable_result = timetable_ripper.execute()
    message_array = [
        "Finished scraping *Regular* timetables. Now looking at _Other_ timetables.\n"
    ]
    message_array.append("_Other_ timetable - ie: IS timetables")
    message = "".join(message_array)
    bot.send_message(chat_id=user_id, text=message, parse_mode="Markdown")
    other_ripper = RipperFactory.get_ripper("Other", username, password)
    other_result = other_ripper.execute()

    message = "Finished scraping *Other* timetables. Now updating database records.."
    bot.send_message(chat_id=user_id, text=message, parse_mode="Markdown")
    # now, you should have a list of both timetable AND other results.
    # timettable_result at this stage should be a List of CLASSES
    # let us merge the two list. for all intends and purposes, we have
    # placed them into an IndividualClassStructure Object, so they are
    # the same to us.
    timetable_result.extend(other_result)
    return timetable_result
