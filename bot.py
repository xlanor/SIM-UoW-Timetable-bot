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
from datetime import datetime
from datetime import timedelta

from telegram.utils.request import Request

# Config file
from cfg import Configuration

# Model imports
from Models.mqbot import MQBot


# Controller imports
import Controllers.Commands.chatbot as Registeration
import Controllers.Commands.update_chatbot as Update
import Controllers.Commands.forget_chatbot as Forget
import Controllers.Commands.retrieve_timetable as tt
import Controllers.Commands.additional_methods as am
import Controllers.Commands.mega as mega
import Controllers.Jobs.reminders as rmd

# Import states from controller
from Controllers.Commands.chatbot import NAME
from Controllers.Commands.chatbot import USERNAME
from Controllers.Commands.chatbot import PASSWORD
from Controllers.Commands.chatbot import APP_KEY
from Controllers.Commands.update_chatbot import ENTERKEY
from Controllers.Commands.update_chatbot import DECRYPT
from Controllers.Commands.forget_chatbot import DELETEUSER


class Hera:
    def __init__(self):
        self.__config = Configuration()
        self.__flush_redis_cache()
        q = mq.MessageQueue(
            all_burst_limit=30,
            all_time_limit_ms=1000,
            group_burst_limit=20,
            group_time_limit_ms=60000,
            exc_route=None,
            autostart=True,
        )
        # set connection pool size for bot
        request = Request(con_pool_size=8)
        self.__queue_bot = MQBot(self.__config.BOT_API_KEY, request=request, mqueue=q)
        self.__updater = Updater(bot=self.__queue_bot)
        self.__dp = self.__updater.dispatcher
        self.__jq = self.__updater.job_queue
        self.__reg()
        self.__update()
        self.__forget()
        self.__timetable()
        self.__ics()
        self.__fuck()
        self.__cbq()
        self.__mega()
        self.__alert()
        self.__nightly()
        self.__toggles()
        self.__help()
        self.__today()
        self.__test_alert()
        self.start_webhooks()  # must always come last.
        print("Bot online")
        print(f"Current Time: {datetime.now()}")

    def add_hello(self):
        """
        A test function.
        """
        # start_handler = CommandHandler('test', self.test)
        start_handler = CommandHandler("test", ct.test_message)
        self.__dp.add_handler(start_handler)

    def __reg(self):
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
            entry_points=[CommandHandler("register", Registeration.start_register)],
            states={
                NAME: [
                    MessageHandler(
                        Filters.text, Registeration.name, pass_user_data=True
                    )
                ],
                USERNAME: [
                    MessageHandler(
                        Filters.text, Registeration.username, pass_user_data=True
                    )
                ],
                PASSWORD: [
                    MessageHandler(
                        Filters.text, Registeration.password, pass_user_data=True
                    )
                ],
                APP_KEY: [
                    MessageHandler(
                        Filters.text, Registeration.application_key, pass_user_data=True
                    )
                ],
            },
            fallbacks=[CommandHandler("cancel", Registeration.cancel)],
            per_user="true",
        )
        self.__dp.add_handler(conv_handler, 1)

    def __update(self):
        update_handler = ConversationHandler(
            entry_points=[CommandHandler("update", Update.update)],
            states={
                ENTERKEY: [
                    RegexHandler("(?iii)Yes", Update.enter_key),
                    RegexHandler("(?iii)No", Update.cancel),
                ],
                DECRYPT: [MessageHandler(Filters.text, Update.decrypt)],
            },
            fallbacks=[CommandHandler("cancel", Update.cancel)],
            per_user="true",
        )
        self.__dp.add_handler(update_handler, 1)

    def __forget(self):
        forget_handler = ConversationHandler(
            entry_points=[CommandHandler("forget", Forget.forget)],
            states={
                DELETEUSER: [
                    RegexHandler("(?iii)Yes", Forget.remove_user),
                    RegexHandler("(?iii)No", Forget.cancel),
                ]
            },
            fallbacks=[CommandHandler("cancel", Forget.cancel)],
            per_user="true",
        )
        self.__dp.add_handler(forget_handler, 1)

    def __timetable(self):
        timetable_handler = CommandHandler("timetable", tt.get_timetable)
        self.__dp.add_handler(timetable_handler, 2)

    def __today(self):
        today_handler = CommandHandler("today", tt.get_today)
        self.__dp.add_handler(today_handler, 2)

    def __ics(self):
        ics_handler = CommandHandler("ics", tt.get_ics)
        self.__dp.add_handler(ics_handler, 2)

    def __fuck(self):
        fuck_handler = CommandHandler("fuck", tt.fuck)
        self.__dp.add_handler(fuck_handler, 2)

    def __cbq(self):
        self.__updater.dispatcher.add_handler(CallbackQueryHandler(tt.get_timetable), 3)

    def __mega(self):

        megaphone_handler = CommandHandler("mega", mega.megaphone)
        self.__dp.add_handler(megaphone_handler, 3)

    def __alert(self):
        # have to set -8 hours UTC time.
        alert_time = datetime.strptime("00:00", "%H:%M").time()
        # self.__jq.run_once(rmd.morning_alert,0)
        job_minute = self.__jq.run_repeating(
            rmd.morning_alert, timedelta(hours=24), alert_time
        )

    def __nightly(self):
        # have to set -8 hours UTC time.
        alert_time = datetime.strptime("14:00", "%H:%M").time()
        # self.__jq.run_once(rmd.nightly_alert,0)
        job_minute = self.__jq.run_repeating(
            rmd.nightly_alert, timedelta(hours=24), alert_time
        )

    def __test_alert(self):
        test_handler = CommandHandler("testrmd", rmd.morning_alert)
        self.__dp.add_handler(test_handler, 3)

    def __toggles(self):
        toggle_morning = CommandHandler("alert", rmd.toggle_morning)
        self.__dp.add_handler(toggle_morning, 2)
        toggle_night = CommandHandler("nightly", rmd.toggle_night)
        self.__dp.add_handler(toggle_night, 2)

    def __help(self):
        help_handler = CommandHandler("help", am.help)
        self.__dp.add_handler(help_handler)

    def __flush_redis_cache(self):
        r = self.__config.REDIS_INSTANCE
        db_flush = r.flushdb()
        print(f"Redis DB Flushed: {db_flush}")

    def start_webhooks(self):
        self.__updater.start_webhook(
            listen="127.0.0.1",
            port=self.__config.webhook_port(),
            url_path=f"{self.__config.BOT_API_KEY}",
        )
        self.__updater.bot.set_webhook(
            url=f"{self.__config.DOMAIN}/{self.__config.BOT_API_KEY}",
            certificate=open(f"{self.__config.LOCATION_OF_CERTS}/cert.pem", "rb"),
        )


if __name__ == "__main__":
    Hera()
