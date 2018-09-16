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
#  A database facade to simplify operations for other controllers.
##
from typing import List
# Internal Model imports.
import Models.db_models as db
from Models.user_object import UserObject
from Models.user_from_db import DbUser

def user_exist(telegram_id:str)->bool:
    user_result = db.getUser(telegram_id)
    if user_result:
        print("found")
        return True
    return False


def insert_new_user(uo:UserObject):
    db.insert_new_user(uo)

def get_user(telegram_id:str)->UserObject:
    telegram_database_user = db.getUser(telegram_id)
    if not telegram_database_user: 
        return None
    else:
        return DbUser(telegram_database_user)

def update_classes(list_of_new_classes:List,telegram_id:str):
    db.resetClasses(telegram_id)
    for new_class in list_of_new_classes:
        db.add_class(telegram_id,new_class)

def delete_user(telegram_id:str):
    return db.del_user(telegram_id)
