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
#  Additional methods that are incorporated into the bot.
##

# 3rd party or native imports
import traceback
import arrow

# Local imports
from cfg import Configuration
from Models.help_message import HelpMessage


def help(bot, update):
    config = Configuration()
    try:
        cid = update.message.chat_id
        message_id = update.message.message_id
        hm = HelpMessage()
        msg = hm.get_help_message()
        print(f"hm:{msg}")
        bot.send_message(
            chat_id=cid,
            text=msg,
            disable_web_page_preview=True,
            reply_to_message_id=message_id,
            parse_mode="Markdown",
        )

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
            chat_id=config.ERROR_CHANNEL, text=f"This message was triggered in help."
        )
