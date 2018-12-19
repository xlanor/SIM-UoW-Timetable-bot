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
#  Methods for the re-sync process.
##
import traceback
import jsonpickle
from telegram.ext import ConversationHandler
import arrow
import traceback


# Local imports
from Models.encryption import Encrypt


# internal Controller imports
import Controllers.db_facade as db_interface

# internal Model imports
from cfg import Configuration

# declares state for subsequent import.
ENTERKEY, DECRYPT = range(2)


def update(bot, update):
    """
    confirms that the update is meant to be handled.
    """
    config = Configuration()
    try:
        uid = update.message.from_user.id
        if not db_interface.user_exist(uid):
            update.message.reply_text("You are not registered! Please register first")
            return ConversationHandler.END
        r = config.REDIS_INSTANCE
        if r.get(uid):
            update.message.reply_text("You are already enqueued in the queue!")
            return ConversationHandler.END
        message_array = ["Do you want to update your timetable?\n"]
        message_array.append("❇️This will erase *all* previous timetable schedules\n")
        message_array.append("❇️Please reply with a yes or no\n")
        message_array.append("❇️To exit this state, please use /cancel\n")
        message = "".join(message_array)
        update.message.reply_text(message, parse_mode="Markdown")
        return ENTERKEY

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
            text=f"This message was triggered in get timetable by {uid}.",
        )
        return ConversationHandler.END


def enter_key(bot, update):
    config = Configuration()
    try:
        message = "Please enter your decryption key\n"
        update.message.reply_text(message, parse_mode="Markdown")
        return DECRYPT

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
            text=f"This message was triggered in enter your decryption key.",
        )
        return ConversationHandler.END


def decrypt(bot, update):
    config = Configuration()
    uid = update.message.from_user.id
    try:
        application_key = update.message.text
        application_key = application_key.strip()
        if not application_key:
            message = "Enter a proper key!\nDo you want to try again? (Yes/No)"
            update.message.reply_text(message, parse_mode="Markdown")
            return ENTERKEY
        else:

            print(uid)
            user_in_db = db_interface.get_user(uid)
            print(user_in_db)
            username = user_in_db.user_name
            decrypted_password = Encrypt(
                user_in_db.encrypted_pass, application_key
            ).decrypt()
            if not decrypted_password:
                message = "A wrong application key has been entered\nDo you want to try again? (Yes/No)"
                update.message.reply_text(message, parse_mode="Markdown")
                return ENTERKEY
            # passes into celery. No longer my problem.
            config = Configuration()
            update_class = config.CELERY_INSTANCE.signature(
                "Controllers.celery_queue.update_user"
            )
            """
            def update_user(
                    telegram_id:str,
                    user_name:str,
                    password:str,
                    bot
                ):
            """
            r = config.REDIS_INSTANCE
            r.set(uid, 1)
            update_class.delay(
                uid, username, decrypted_password, jsonpickle.encode(bot)
            )
            message = "Your details have been enqueued for scraping!\nThis process might take up to 5 minutes, please wait for the results."
            update.message.reply_text(message, parse_mode="Markdown")
            return ConversationHandler.END
    except Exception as e:
        update.message.reply_text("Unknown error occured", parse_mode="Markdown")
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
        return ConversationHandler.END


def cancel(bot, update):
    """
    Cancels the chatbot process.
    """
    message = "Cancelling update! Goodbye"
    update.message.reply_text(message, parse_mode="Markdown")
    return ConversationHandler.END
