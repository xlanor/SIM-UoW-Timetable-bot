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
from datetime import datetime
# Internal Model imports.
import Models.db_models as db
from Models.user_object import UserObject
from Models.user_from_db import DbUser
from Models.classes import IndividualClassStructure

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

def get_current_class(telegram_id:str,start_date,end_date):
    """
    {
        "_id" : null,
        "classes" : [ 
            {
                "class_name" : "NTR 110 - Nutrition in Practice Lab",
                "date" : ISODate("2018-09-21T00:00:00.000Z"),
                "day" : "Friday",
                "numeric_day" : 4,
                "start_time" : ISODate("2018-09-21T12:00:00.000Z"),
                "end_time" : ISODate("2018-09-21T14:00:00.000Z"),
                "location" : "HQ BLK A SR A.4.09A",
                "type" : "Lecture"
            }....
        ]
    }
    """
    aggregation_result = db.get_classes_as_object(telegram_id,start_date,end_date)
    result_list = []
    if aggregation_result:
        for class_list in aggregation_result:
            try:
                for found_class in class_list["classes"]:
                    ic = IndividualClassStructure("")
                    ic.set_from_dict(found_class)
                    result_list.append(ic)
            except KeyError:
                print("NO classes, pass")
                pass
       
    return result_list


def get_last_sync_date(telegram_id:str):
    user_result = db.getUser(telegram_id)
    lsd = user_result["last_synced_date"]
    return datetime.strftime(lsd, '%b %d %Y %H:%M')

def check_if_exist(type:str,telegram_id:str,current_date):
    if type == "previous":
        result = db.get_earlier_date(telegram_id,current_date)
    else:
        result = db.get_later_date(telegram_id,current_date)
    
    return list(result)
