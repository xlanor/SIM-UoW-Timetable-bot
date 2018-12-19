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
#   Megaphones!
##
from telegram.error import Unauthorized
import arrow
import traceback

# internal Controller imports
import Controllers.db_facade as db_interface

# internal Model imports
from cfg import Configuration


def megaphone(bot, update):
    uid = update.message.from_user.id
    config = Configuration()
    try:
        message = update.message.text[6:]
        if str(uid) in config.ADMIN_LIST:
            list_of_ids = db_interface.get_all_telegram_ids()
            count = 0
            for id in list_of_ids:
                try:
                    bot.send_message(chat_id=id, text=message, parse_mode="HTML")
                    count += 1
                except Unauthorized:
                    pass

            bot.send_message(
                chat_id=config.ERROR_CHANNEL, text=f"{count} messages megaphoned"
            )
        else:
            update.message.reply_text("You are not an administrator!")
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
            text=f"This message was triggered in megaphone.",
        )
