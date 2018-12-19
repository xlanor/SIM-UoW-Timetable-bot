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
# User Object. This Object will prepare the data retrieved from the
# signup process for insertiopn into mongodb.
##
# Native or 3rd party lib imports
from typing import List
from typing import Dict
from datetime import datetime
from datetime import timedelta


class UserObject:
    def __init__(self, telegram_id: int, username: str, name: str, encrypted_pass):
        self.__telegram_id = telegram_id
        self.__username = username
        self.__name = name
        self.__encrypted_pass = encrypted_pass
        self.__classes = []

    def add_classes(self, list_of_classes: List):
        self.__classes.extend(list_of_classes)

    def get_class_leng(self) -> int:
        return len(self.__classes)

    def get_mongo_dict(self) -> Dict:
        class_list = [x.get_dict_mongo() for x in self.__classes]
        # we will now enable both by default.
        generated_dict = {
            "telegram_id": self.__telegram_id,
            "username": self.__username,
            "name": self.__name,
            "encrypted_pass": self.__encrypted_pass,
            "class_list": class_list,
            "last_synced_date": datetime.now() + timedelta(hours=8),
            "alert": True,
            "nightly_alert": True,
        }
        return generated_dict
