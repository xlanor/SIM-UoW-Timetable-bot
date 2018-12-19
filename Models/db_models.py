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
#   Database pertaining classes or methods
##

# 3rd party/native Library Modules
import pymongo
from pymongo import MongoClient
from datetime import datetime
from datetime import timedelta
from datetime import date
from datetime import time
from typing import Dict

# Local models imports
from Models.singleton_sp import Singleton
from Models.classes import IndividualClassStructure
from Models.user_object import UserObject
from cfg import Configuration

# A singleton class to instantiate a db object once and reuse throughout.
# PyMongo defaults to a connection pool.
class MongoDB(metaclass=Singleton):
    def __init__(self):
        self.__cfg = Configuration()
        # Instantiated only ONCE will reuse throughout connection
        self.__mongo = MongoClient(self.__cfg.MONGOURI)
        self.__db = self.__mongo.timetable

    @property
    def client(self):
        return self.__mongo

    @property
    def db(self):
        return self.__db


def getUser(telegram_id: str):
    mdb = MongoDB().db
    return mdb.tgbot_records.find_one({"telegram_id": telegram_id})


def resetClasses(telegram_id: str):
    mdb = MongoDB().db
    mdb.tgbot_records.update({"telegram_id": telegram_id}, {"$set": {"class_list": []}})


def update_last_sync_date(telegram_id: str):
    mdb = MongoDB().db
    mdb.tgbot_records.update(
        {"telegram_id": telegram_id}, {"$set": {"last_synced_date": datetime.now()}}
    )


def add_class(telegram_id: str, class_object: IndividualClassStructure):
    mdb = MongoDB().db
    class_dict = class_object.get_dict_mongo()
    mdb.tgbot_records.update(
        {"telegram_id": telegram_id}, {"$push": {"class_list": class_dict}}
    )


def insert_new_user(user_obj: UserObject):
    mdb = MongoDB().db
    mdb.tgbot_records.insert(user_obj.get_mongo_dict())


def del_user(telegram_id: str) -> int:
    mdb = MongoDB().db
    result = mdb.tgbot_records.delete_one({"telegram_id": telegram_id})
    return result


def get_classes_as_object(telegram_id: str, start_date, end_date):
    mdb = MongoDB().db
    return mdb.tgbot_records.aggregate(
        [
            {"$unwind": "$class_list"},
            {
                "$match": {
                    "$and": [
                        {"telegram_id": telegram_id},
                        {"class_list.date": {"$gte": start_date, "$lte": end_date}},
                    ]
                }
            },
            {"$group": {"_id": None, "classes": {"$push": "$class_list"}}},
        ]
    )


def get_later_date(telegram_id: str, current_date):
    mdb = MongoDB().db
    return mdb.tgbot_records.aggregate(
        [
            {"$unwind": "$class_list"},
            {
                "$match": {
                    "$and": [
                        {"telegram_id": telegram_id},
                        {"class_list.date": {"$gt": current_date}},
                    ]
                }
            },
            {"$group": {"_id": "null", "count": {"$sum": 1}}},
        ]
    )


def get_earlier_date(telegram_id: str, current_date):
    mdb = MongoDB().db
    return mdb.tgbot_records.aggregate(
        [
            {"$unwind": "$class_list"},
            {
                "$match": {
                    "$and": [
                        {"telegram_id": telegram_id},
                        {"class_list.date": {"$lt": current_date}},
                    ]
                }
            },
            {"$group": {"_id": "null", "count": {"$sum": 1}}},
        ]
    )


def get_telegram_users():
    mdb = MongoDB().db
    return mdb.tgbot_records.distinct("telegram_id", {"telegram_id": {"$exists": True}})


def find_all_users():
    mdb = MongoDB().db
    return mdb.tgbot_records.find()


def find_all_users_by_alert(user_type: str):
    mdb = MongoDB().db
    if user_type.lower() == "morning":
        return mdb.tgbot_records.find({"alert": True})
    else:

        return mdb.tgbot_records.find({"nightly_alert": True})


def update_alert(telegram_id: str, type_to_change: bool):
    mdb = MongoDB().db
    mdb.tgbot_records.update(
        {"telegram_id": telegram_id}, {"$set": {"alert": type_to_change}}
    )


def update_nightly(telegram_id: str, type_to_change: bool):
    mdb = MongoDB().db
    mdb.tgbot_records.update(
        {"telegram_id": telegram_id}, {"$set": {"nightly_alert": type_to_change}}
    )


def update_last_sync(telegram_id: str, new_date: date):
    mdb = MongoDB().db
    mdb.tgbot_records.update(
        {"telegram_id": telegram_id}, {"$set": {"last_synced_date": new_date}}
    )
