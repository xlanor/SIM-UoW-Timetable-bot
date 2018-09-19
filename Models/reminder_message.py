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
#  Model for the reminder message
##
from datetime import datetime
from datetime import timedelta
from typing import List
class ReminderMessage():
    def __init__(self,
            list_of_classes:str,
            type_of_reminder:str,
            name:str,
            date_to_show
        ):
        self.__name = name
        self.__list_of_classes = list_of_classes

        self.__list_of_classes.sort(key = lambda x: x.start_time)
        self.__reminder_type = type_of_reminder
        self.__date = date_to_show
    
    def get_message(self)->str:
        message_array = []
        if self.__reminder_type == "Morning":
            message_array.append(f"Good Morning {self.__name}\n")
        else:
            message_array.append(f"Good Evening {self.__name}\n")
        message_array.append("These are your classes for ")
        
        if self.__reminder_type == "Morning":
            message_array.append("*Today*, ")
        else:
            message_array.append("*Tomorrow*, ")
        message_array.append(f"{self.__date}\n\n")

        if self.__reminder_type == "Morning":
            day_name = datetime.today().strftime("%A")
        else:
            day_name = ((datetime.today())+timedelta(1)).strftime("%A")
        message_array.append(f"📅 *{day_name}*\n")

        if len(self.__list_of_classes) == 0:
            message_array.append("```-```\n\n")
        else:
            for class_object in self.__list_of_classes:
                message_array.append(class_object.get_formatted_text())
                message_array.append("\n")
        message_array.append("\n")
        
        if self.__reminder_type == "Morning":
            toggle = "/alert"
        else:
            toggle = "/nightly"
        message_array.append(f"To unsubscribe from this reminder, please use {toggle}")
        return "".join(message_array)