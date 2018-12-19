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
# This contains the method for removing users from the database.
##
# 3rd party or native import
from telegram.ext import ConversationHandler

# internal Controller imports
import Controllers.db_facade as db_interface

# internal Model imports
from cfg import Configuration

# from celery_queue import register_user
from Models.encryption import Encrypt

DELETEUSER = range(1)


def forget(bot, update):
    try:
        message_array = ["Do you want to *erase all * your details?\n"]
        message_array.append("Please reply with a yes or no (case-insensetive)")
        message = "".join(message_array)
        update.message.reply_text(message, parse_mode="Markdown")
        return DELETEUSER

    except Exception as e:
        print(str(e))  # To be changed.
        return ConversationHandler.END


def remove_user(bot, update):
    try:
        uid = update.message.from_user.id
        print(db_interface.user_exist(uid))
        if db_interface.user_exist(uid):
            delete_result = db_interface.delete_user(uid)
            message_array = []
            if delete_result.deleted_count == 1:
                message_array.append(
                    f"Details for {uid} has been removed from the database\n"
                )
                message_array.append("You can now register again using /register")
            else:
                message_array.append(
                    "An Unknown error has occured! Kindly inform @fatalityx"
                )
            message = "".join(message_array)
            update.message.reply_text(message, parse_mode="Markdown")
        else:
            message_array = [
                f"Unable to find your telegram ID {uid} in the database!\n"
            ]
            message_array.append("Are you sure you didn't mean to register instead?")
            message = "".join(message_array)
            update.message.reply_text(message, parse_mode="Markdown")
    except Exception as e:
        print(str(e))  # To be changed.
        return ConversationHandler.END


def cancel(bot, update):
    """
    Cancels the chatbot process.
    """
    message = "Cancelling registeration! Goodbye"
    update.message.reply_text(message, parse_mode="Markdown")
    return ConversationHandler.END
