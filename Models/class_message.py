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
# Class message for retrival of timetable.
##
from Models.classes import IndividualClassStructure
import calendar
class MessageTimetable():
    GITHUB_URL = "https://github.com/xlanor/SIM-UoW-Timetable-bot/blob/master/DISCLAIMER.md"
    def __init__(self,cur_week:str,last_sync_date:str):
        self.__cur_week = cur_week
        self.__last_sync_date = last_sync_date
        # prepares a nested list of lists.
        self.__class_list = []
        for i in range(7):
            self.__class_list.append([])

    
    def add_class_list(self,
                    class_numeric_day:int,
                    class_object:IndividualClassStructure
                ):
        self.__class_list[class_numeric_day].append(class_object)
        
    
    def get_message(self):
        message_array = [f"📈Timetable for the week of *{self.__cur_week}*\n"]
        message_array.append(f"🔃 This timetable was last synced on *{self.__last_sync_date}*\n")
        message_array.append(f"By using this bot, you agree to the terms and conditions stated in the [DISCLAIMER.md]({MessageTimetable.GITHUB_URL}) on github\n\n")
        for i in range(7):
            message_array.append(f"󠁳📅 *{calendar.day_name[i]}*\n")
            if len(self.__class_list[i]) == 0:
                message_array.append("📌-\n")
                message_array.append("```")
                message_array.append(" You have no classes for this day!")
                message_array.append("```\n")
            else:
                for class_object in self.__class_list[i]:
                    message_array.append(class_object.get_formatted_text())
                    message_array.append("\n")
            message_array.append("```==============```\n")
            message_array.append("\n")
        return "".join(message_array)
