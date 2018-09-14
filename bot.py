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

import celery_test as ct

# Controller imports
import Controllers.Commands.chatbot as Registeration
# Import states from controller
from Controllers.Commands.chatbot import NAME
from Controllers.Commands.chatbot import USERNAME
from Controllers.Commands.chatbot import PASSWORD
from Controllers.Commands.chatbot import APP_KEY

class Hera():
    def __init__(self):
        self.__config = Configuration()
        q = mq.MessageQueue(
                all_burst_limit=3, 
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
        self.reg()
        self.start_webhooks() # must always come last.
        print("Bot online")
    
    def add_hello(self):
        """
        A test function.
        """
        #start_handler = CommandHandler('test', self.test)
        start_handler = CommandHandler('test', ct.test_message)
        self.__dp.add_handler(start_handler)

    def reg(self):
        """
        The accumulated user data will be passed through the respective states
        at the end, it will be passed into celery.
        Previously, in Cronus (v1), we actually adopted an approach of 
        repeatedly checking the account credentials on signup.
        In v2, we have delegated that to celery - the user will simply have to re-register if the wrong credentials are provided.
        Only after the registeration process has successfully completed, then and only
        then will their credentials be stored in the database.
        """
        conv_handler = ConversationHandler(
            entry_points = [CommandHandler('register',Registeration.start_register)],

            states = {
                NAME: [MessageHandler(
                                    Filters.text,
                                    Registeration.name,
                                    pass_user_data=True
                                )
                        ],
                USERNAME: [MessageHandler(
                                    Filters.text,
                                    Registeration.username,
                                    pass_user_data=True
                                )
                        ],
                PASSWORD: [MessageHandler(
                                    Filters.text,
                                    Registeration.password,
                                    pass_user_data=True
                                )
                        ],
                APP_KEY: [MessageHandler(
                                    Filters.text,
                                    Registeration.application_key,
                                    pass_user_data=True
                                )
                        ]
            },
            fallbacks=[CommandHandler('cancel', Registeration.cancel)],
            per_user = 'true'
        )
        self.__dp.add_handler(conv_handler,1)


    def start_webhooks(self):
        self.__updater.start_webhook(
                            listen='127.0.0.1', 
                            port=self.__config.webhook_port(), 
                            url_path=f'{self.__config.BOT_API_KEY}'
                        )
        self.__updater.bot.set_webhook(url=f'{self.__config.DOMAIN}/{self.__config.BOT_API_KEY}',
                        certificate=open(f'{self.__config.LOCATION_OF_CERTS}/cert.pem', 'rb'))


if __name__ == "__main__":
    Hera()

