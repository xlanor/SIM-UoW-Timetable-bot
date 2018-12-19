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
#   Configuration class file held in a singleton.
##
from Models.singleton_sp import Singleton
from celery import Celery
import redis


class Configuration(metaclass=Singleton):
    def __init__(self):
        self.BOT_API_KEY = ""  # Your api token here
        self.IS_STAGING = True
        self.ERROR_CHANNEL = ""  # Your error channel token here
        self.ADMIN_LIST = ["YOUR_TELEGRAM_ID"]
        self.STAGING_PORT = 0  # Your port number here
        self.PRODUCTION_PORT = 1  # Your port number here
        self.LOCATION_OF_CERTS = (
            "/some/absolute/pathing/here"
        )  # path to certificates for nginx (pem and cert, generated via openssl.)
        self.DOMAIN = "https://your.doma.in"  # domain for webhook.
        self.MONGOURI = "YOURMONGOURI"
        self.CELERY_INSTANCE = Celery(include=["Controllers.celery_queue"])
        self.REDIS_INSTANCE = redis.StrictRedis(
            """POPULATE WITH YOUR REDIS INFORMATION"""
        )
        self.AUTHOR_TELEGRAM = "YOURTELEID"
        self.AUTHOR_EMAIL = "YOUR@EMAIL.ADDRESS"
        self.AUTHOR_TELEGRAM_ID = 1234567  # YOURTGID
        self.GITHUB_URL = "https://github.com/xlanor/SIM-UoW-Timetable-bot"

    def is_admin(self, id_to_check: str) -> bool:
        if id_to_check in self.ADMIN_LIST:
            return True

    def webhook_port(self):
        if self.IS_STAGING:
            return self.STAGING_PORT
        return self.PRODUCTION_PORT
