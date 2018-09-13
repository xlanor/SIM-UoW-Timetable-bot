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


# Local Imports 
from Controllers.Ripper.ripper import RipperFactory
import Controllers.db_facade as dbInterface
from Models.exceptions import *
from Models.user_object import UserObject


def register_user(user_data:Dict, bot):
    try:
        user_id = user_data["user_id"]
        username = user_data["username"]
        password = user_data["password"]
        name = user_data["name"]
        encrypted_password = user_data["encrypted_password"]
        try:
            # Able to login with given credentials.
            timetable_ripper = RipperFactory.get_ripper("NewRip",username,password)
            timetable_result = timetable_ripper.execute()
            other_ripper = RipperFactory.get_ripper("Other",username,password)
            other_result = other_ripper.execute()
            # now, you should have a list of both timetable AND other results.
            # timettable_result at this stage should be a List of CLASSES
            # let us merge the two list. for all intends and purposes, we have
            # placed them into an IndividualClassStructure Object, so they are 
            # the same to us.
            timetable_result.extend(other_result)
            # Now, let us begin constructing our database insertion object.
            obj_to_insert = UserObject(
                                    user_id,
                                    username,
                                    password,
                                    name,
                                    encrypted_password
                                )
            obj_to_insert.add_classes(timetable_result)
            dbInterface.insert_new_user(obj_to_insert)
            success_message=[f"A total of {obj_to_insert.get_class_leng()} records have been synced to the database\n"]
            success_message.append("You can now use /timetable to retrieve your timetable\n")
            success_message.append("In addition, please take note of the following handlers:\n")
            success_message.append("```/alert - Daily reminder at 7am in the morning```\n")
            success_message.append("```/nightly - Nightly reminder at 10pm at night\n")
            success_message.append("Both of these handlers act as a toggle.")
            message = "".join(success_message)
            bot.send_message(
                    chat_id = user_id,
                    text = message,
                    parse_mode = 'Markdown'
                )

        except UnableToLogin:
            # Unable to login with given credentials.
            # new_ripper attempts to login and raises an UnableToLogin exception
            # if it cant be logged in.
            error_message = ["Unable to login with your credentials!\n"]
            error_message.append("Please try to register again using /register")
            err = "".join(error_message)
            bot.send_message(
                        chat_id = user_id,
                        text = err,
                        parse_mode = 'Markdown'
                    )
    except Exception as e:
        # to send to github
        print(str(e))
        pass
