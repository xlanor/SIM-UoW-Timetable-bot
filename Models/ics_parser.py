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
# ICS Class for getting an ICS file from mongo.
##
# Third party libraries
from ics import Calendar, Event
import arrow

# Internal imports
from Models.classes import IndividualClassStructure


class ICSParser:
    def __init__(self, class_list: [IndividualClassStructure]):
        self.__class_list = class_list
        self.__calendar = Calendar()

    @property
    def calendar(self) -> Calendar:
        return self.__calendar

    def convert_to_event(self):
        for period in self.__class_list:
            e = Event()
            e.name = period.name
            e.begin = period.ics_formatted_plus_eight_start
            e.end = period.ics_formatted_plus_eight_end
            e.location = period.location
            e.description = period.class_type
            self.__calendar.events.add(e)
