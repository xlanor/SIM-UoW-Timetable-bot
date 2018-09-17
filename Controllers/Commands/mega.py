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

# internal Controller imports
import Controllers.db_facade as db_interface

# internal Model imports
from cfg import Configuration

def megaphone(bot,update):
    uid = update.message.from_user.id
    try:
        message = update.message.text[6:]
        config = Configuration()
        if str(uid) in config.ADMIN_LIST:
            list_of_ids = db_interface.get_all_telegram_ids()
            for id in list_of_ids:
                try:
                    bot.send_message(
                            chat_id = id,
                            text = message,
                            parse_mode='HTML'
                    )
                except Unauthorized:
                    pass
        else:
            update.message.reply_text("You are not an administrator!")
    except Exception as e:
        print(str(e))
        # to be changed
        pass