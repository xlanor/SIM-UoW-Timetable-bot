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
# User Object. This Object will be for users retrieved from the database.
##
# native/3rd party lib imports
from typing import Dict
from datetime import date

#local imports
from Models.classes import IndividualClassStructure
class DbUser():
    def __init__(self, retrieved_user:Dict):
        self.telegram_id = retrieved_user["telegram_id"]
        self.name = retrieved_user["name"]
        self.user_name = retrieved_user["username"]
        self.encrypted_pass = retrieved_user["encrypted_pass"]
        self.last_synced_date = retrieved_user["last_synced_date"]
        self.alert = False
        self.nightly = False
        self.raw_class_list = retrieved_user["class_list"]
        self.class_list = []
        try:
            self.alert = retrieved_user["alert"]
        except KeyError:
            self.alert = True
        try:
            self.nightly = retrieved_user["nightly_alert"]
        except KeyError:
            self.nightly = False
        self.__process_class()
    
    def __process_class(self):
        for classes in self.raw_class_list:
            ic = IndividualClassStructure("")
            ic.set_from_dict(classes)
            self.class_list.append(ic)
    
    def get_list_of_class_by_date(self,date_object):
        return_list = []
        for class_obj in self.class_list:
            if class_obj.date.date() == date_object:
                return_list.append(class_obj)
        return return_list
