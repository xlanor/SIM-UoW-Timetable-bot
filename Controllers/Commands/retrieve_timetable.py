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
# Methods for retrival of timetable
##

# Internal library imports
from datetime import datetime
from datetime import timedelta
from datetime import date
from datetime import time
import traceback

# Third party library imports
from telegram import InlineKeyboardButton
from telegram import InlineKeyboardMarkup
import pytz
import arrow

# Internal Imports
from cfg import Configuration
from Models.class_message import MessageTimetable
from Models.ics_parser import ICSParser
import Controllers.db_facade as db_interface


def get_timetable(bot, update):
    config = Configuration()
    is_callback = False
    if not update.message:
        uid = update.callback_query.from_user.id
        is_callback = True
    else:
        uid = update.message.from_user.id
    try:
        if db_interface.user_exist(uid):
            # if its not a callback type:
            if not is_callback:
                current_date = date.today()
                # sets time to midnight.
                current_date = datetime.combine(current_date, time())
            else:  # if it is a callback
                query = update.callback_query
                current_date = datetime.strptime(query.data[2:], "%b%d%Y")

            start_date = current_date - timedelta(days=current_date.weekday())
            end_date = start_date + timedelta(days=6)

            # gets a list of IndividualClassStructure objects.
            classes_list = db_interface.get_current_class(uid, start_date, end_date)
            # sorts by start time
            classes_list.sort(key=lambda x: x.start_time)
            lsd = db_interface.get_last_sync_date(uid)

            # prepares the message timetable object
            cur_week = datetime.strftime(
                (current_date - timedelta(days=current_date.weekday())), "%b %d %Y"
            )
            print(cur_week)
            mt = MessageTimetable(cur_week, lsd)
            for c in classes_list:
                mt.add_class_list(c.class_numeric_day, c)
            formatted_message = mt.get_message()

            # prepares the keyboard.
            reply_kb = get_keyboard(uid, current_date, start_date, end_date)
            reply_markup = InlineKeyboardMarkup(reply_kb)
            # sends the message
            if is_callback:
                bot.edit_message_text(
                    text=formatted_message,
                    chat_id=update.callback_query.message.chat_id,
                    message_id=update.callback_query.message.message_id,
                    disable_web_page_preview=True,
                    reply_markup=reply_markup,
                    parse_mode="Markdown",
                )
            else:
                update.message.reply_text(
                    formatted_message,
                    reply_markup=reply_markup,
                    disable_web_page_preview=True,
                    quote=True,
                    parse_mode="Markdown",
                )
        else:
            message_array = [f"Unable to find telegram ID {uid} in our database\n"]
            message_array.append(
                "Kindly register using /register before attempting to retrieve a timetable."
            )
            message = "".join(message_array)
            update.message.reply_text(message, parse_mode="Markdown")

    except Exception as e:
        print(str(e))
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
            text=f"This message was triggered in get timetable by {uid}.",
        )


def get_today(bot, update):
    uid = update.message.from_user.id
    config = Configuration()

    try:
        if db_interface.user_exist(uid):
            current_date = datetime.now(pytz.timezone("Asia/Singapore")).date()
            # sets time to midnight.
            current_date = datetime.combine(current_date, time())
            # gets a list of IndividualClassStructure objects.
            classes_list = db_interface.get_current_class(
                uid, current_date, current_date
            )
            # sorts by start time
            classes_list.sort(key=lambda x: x.start_time)
            lsd = db_interface.get_last_sync_date(uid)

            mt = MessageTimetable(None, lsd)
            for c in classes_list:
                mt.add_class_list(c.class_numeric_day, c)
            formatted_message = mt.get_today()

            update.message.reply_text(
                formatted_message,
                disable_web_page_preview=True,
                quote=True,
                parse_mode="Markdown",
            )

        else:
            message_array = [f"Unable to find telegram ID {uid} in our database\n"]
            message_array.append(
                "Kindly register using /register before attempting to retrieve a timetable."
            )
            message = "".join(message_array)
            update.message.reply_text(message, parse_mode="Markdown")

    except Exception as e:
        print(str(e))
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
            text=f"This message was triggered in get today timetable by {uid}.",
        )


def get_keyboard(tg_id: str, current_date, start_date, end_date):
    keyboard = []
    nested_keyboard = []
    # prepare for callback.
    previous_start_date = start_date - timedelta(days=7)
    previous_end_date = end_date - timedelta(days=7)
    next_start_date = start_date + timedelta(days=7)
    next_end_date = end_date + timedelta(days=7)

    is_previous = db_interface.check_if_exist("previous", tg_id, current_date)
    is_next = db_interface.check_if_exist("next", tg_id, current_date)
    print(is_next)

    if is_previous:
        previous_date_trigger = f"pr{datetime.strftime(previous_start_date,'%b%d%Y')}"
        nested_keyboard.append(
            InlineKeyboardButton(
                "⬅️ Previous Week", callback_data=previous_date_trigger
            )
        )

    if is_next:
        next_date_trigger = f"nx{datetime.strftime(next_start_date,'%b%d%Y')}"
        nested_keyboard.append(
            InlineKeyboardButton("Next Week ➡", callback_data=next_date_trigger)
        )

    cd = date.today()
    # sets time to midnight.
    cd = datetime.combine(cd, time())
    today_date_trigger = f"td{datetime.strftime(cd,'%b%d%Y')}"
    today_date_keyboard = [
        InlineKeyboardButton("This Week ⬆ ️", callback_data=today_date_trigger)
    ]
    keyboard.append(nested_keyboard)
    keyboard.append(today_date_keyboard)
    return keyboard


def fuck(bot, update):
    config = Configuration()
    uid = update.message.from_user.id
    try:
        if db_interface.user_exist(uid):
            current_date = date.today()
            # sets time to midnight.
            current_date = datetime.combine(current_date, time())

            start_date = current_date - timedelta(days=current_date.weekday())
            end_date = start_date + timedelta(days=6)

            # gets a list of IndividualClassStructure objects.
            classes_list = db_interface.get_current_class(uid, start_date, end_date)
            # sorts by start time
            classes_list.sort(key=lambda x: x.start_time)
            lsd = db_interface.get_last_sync_date(uid)

            # prepares the message timetable object
            cur_week = datetime.strftime(
                (current_date - timedelta(days=current_date.weekday())), "%b %d %Y"
            )
            print(cur_week)
            mt = MessageTimetable(cur_week, lsd)
            for c in classes_list:
                mt.add_class_list(c.class_numeric_day, c)
            formatted_message = mt.get_fucked()

            # sends the message
            update.message.reply_text(
                formatted_message,
                disable_web_page_preview=True,
                quote=True,
                parse_mode="Markdown",
            )
        else:
            message_array = [f"Unable to find telegram ID {uid} in our database\n"]
            message_array.append(
                "Kindly register using /register before attempting to retrieve a timetable."
            )
            message = "".join(message_array)
            update.message.reply_text(message, parse_mode="Markdown")

    except Exception as e:
        print(str(e))
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
            text=f"This message was triggered in get fucked timetable by {uid}.",
        )


def get_ics(bot, update):
    print("Get ICS method called")
    config = Configuration()
    is_callback = False
    if not update.message:
        uid = update.callback_query.from_user.id
        is_callback = True
    else:
        uid = update.message.from_user.id
    try:
        if db_interface.user_exist(uid):
            print("DB Interface exists")
            filepath = f"./ics/{uid}.ics"
            # Gets a list of classes
            classes_list = db_interface.get_all_classes(uid)
            print(classes_list)
            ics_model = ICSParser(classes_list)
            ics_model.convert_to_event()
            with open(filepath, "w") as f:
                f.writelines(ics_model.calendar)

            # sends the message
            bot.send_document(chat_id=uid, document=open(filepath, "rb"))
        else:
            message_array = [f"Unable to find telegram ID {uid} in our database\n"]
            message_array.append(
                "Kindly register using /register before attempting to retrieve a timetable."
            )
            message = "".join(message_array)
            update.message.reply_text(message, parse_mode="Markdown")

    except Exception as e:
        print(str(e))
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
            text=f"This message was triggered in get timetable by {uid}.",
        )
