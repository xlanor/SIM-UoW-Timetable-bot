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
#   Main entry point for Minvera.
##

# PTB imports.
import telegram
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import CallbackQueryHandler
from telegram.ext import Job
from telegram.ext import MessageHandler
from telegram.ext import Filters
from telegram.ext import RegexHandler
from telegram.ext import ConversationHandler
from telegram.ext import messagequeue as mq

from telegram.utils.request import Request

# Config file
from cfg import Configuration

# Model imports
from Models.mqbot import MQBot

# Controller imports

class Minvera():
    def __init__(self):
        self.__config = Configuration()
        q = mq.MessageQueue(
                all_burst_limit=30, 
                all_time_limit_ms=1000, 
                group_burst_limit=20, 
                group_time_limit_ms=60000, 
                exc_route=None, 
                autostart=True
            )
        # set connection pool size for bot 
        request = Request(con_pool_size=8)
        self.__queue_bot = MQBot(self.__config.BOT_API_KEY,request = request, mqueue = q)
        self.__updater = Updater(bot = self.__queue_bot)
        self.__dp = self.__updater.dispatcher
        self.add_hello()
        self.start_webhooks() # must always come last.
        print("Bot online")
    
    def add_hello(self):
        start_handler = CommandHandler('test', self.test)
        self.__dp.add_handler(start_handler)
    
    """
    A test function
    """
    def test(self,bot,update):
        print(bot)
        print(update)
        chat_id = update.message.chat_id
        for i in range(10):
            bot.send_message(chat_id= chat_id, text = "Hello,world!")

    def start_webhooks(self):
        self.__updater.start_webhook(
                            listen='127.0.0.1', 
                            port=self.__config.webhook_port(), 
                            url_path=f'{self.__config.BOT_API_KEY}'
                        )
        self.__updater.bot.set_webhook(url=f'{self.__config.DOMAIN}/{self.__config.BOT_API_KEY}',
                        certificate=open(f'{self.__config.LOCATION_OF_CERTS}/cert.pem', 'rb'))
"""
def mega(bot,update):
    print(bot)
    print(update)
config = Configuration()
print(config.__dict__)
updater = Updater(token=config.BOT_API_KEY)
dispatcher = updater.dispatcher

start_handler = CommandHandler('mega', mega)
self.__dp.add_handler(start_handler)
updater.start_webhook(listen='127.0.0.1', port=config.webhook_port(), url_path=f'{config.BOT_API_KEY}')

updater.bot.set_webhook(url=f'https://do.jingk.ai/{config.BOT_API_KEY}',
                        certificate=open(f'{config.LOCATION_OF_CERTS}/cert.pem', 'rb'))"""

if __name__ == "__main__":
    Minvera()
