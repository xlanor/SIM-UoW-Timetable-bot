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
#   Model to hold class time.
#   Written by xlanor
##

import time as clock
from bs4 import BeautifulSoup
import re


class IndividualClassStructure():
    def __init__(self, name):
        self.__name = name
        # Initialize a few empty holding vars.
        self.__date = ""
        self.__starttime = ""
        self.__endtime = ""
        self.__location = ""
        self.__class_type = ""
    """
        Gets the variables in a dictionary format.
    """
    def get_dict(self):
        return_dict = {
                        "class_name": self.__name,
                        "date": self.__date,
                        "Start_Time": self.__starttime,
                        "End_Time": self.__endtime,
                        "Location": self.__location,
                        "Type": self.__class_type
                        }
        return return_dict

    def get_name(self):
        return self.__name

    def get_date(self):
        return self.__date

    def get_loc(self):
        return self.__location

    def get_start_time(self):
        return self.__starttime

    def get_end_time(self):
        return self.__endtime

    def get_class_type(self):
        return self.__class_type

    """
        Gets the dates of classes, strips it and reformats it.
        @params row, a row pulled from the html
    """
    def set_date_of_class(self, row):
        getdate = row.find("span",
                           {
                              'id': re.compile(r'(MTG_DATES\$)([0-9]{1})')
                           }
                           )
        if not getdate.text.strip():
            getdate = row.find("span",
                               {
                                  'id': re.compile(r'(MTG_DATES\$)([0-9]{1})([0-9]{1})')  # noqa
                               }
                               )

        # date is returned in the format DD/MM/YYYY - DD/MM/YYYY
        # because the end date is redundant
        # (unless SIM decides to hold 24hr overnight classes)

        date = getdate.text
        # strips spaces, splits by -, returns first date.
        strippeddate = (((date.strip()).split("-"))[0]).strip()

        self.__date = strippeddate

    """
        Sets the start/endtime of the class object.
        @params type, true if start time else end time.
        @params row, a row object pulled from the html.

    """
    def set_time(self, class_type, row):
        if class_type:
            self.__starttime = "{} {}".format(self.__date,
                                              self.__get_time(class_type, row))
        else:
            self.__endtime = "{} {}".format(self.__date,
                                            self.__get_time(class_type, row))

    """
        Sets the location of the class object
        @params row, the row scraped from the html.
    """
    def set_location(self, row):
        getlocation = row.find("span",
                               {
                                   'id': re.compile(r'(MTG_LOC\$)([0-9]{1})')
                               }
                               )
        if not getlocation.text.strip():
            getlocation = row.find("span",
                                   {
                                       'id': re.compile(r'(MTG_LOC\$)([0-9]{1})([0-9]{1})')  # noqa
                                   }
                                   )

        self.__location = getlocation.text

    """
        Sets the class type of the class object.
        @params list_of_class_type_keys, a list of all the class keys.
        @params class_type_dict, a dictionary of the class types
        @params no of keys, the total number of keys
        @params rowid, the current rowid.
    """

    def determine_class_type(self, list_of_class_type_keys,
                             class_type_dict, no_of_keys, rowid):
        counter = 0
        trigger = True
        while trigger:
            actual_class_type = ""
            if int(rowid) >= int(list_of_class_type_keys[counter]):
                actual_class_type = class_type_dict[list_of_class_type_keys[counter]]  # noqa
                counter += 1
                if counter >= (no_of_keys):
                    trigger = False
            else:
                trigger = False
        # Fixes SIMConnect's spelling error.
        if actual_class_type == "Consultati":
            actual_class_type = "Consultation"
        self.__class_type = actual_class_type

    """################################################

                BEGIN PRIVATE METHODS

    ################################################"""

    """
        Get the time.
        @params type, true if start time else end time.
        @params row, a row object pulled from the html.
    """
    def __get_time(self, type, row):
        gettime = row.find("span",
                           {
                               'id': re.compile(r'(MTG_SCHED\$)([0-9]{1})')
                           }
                           )
        if not gettime.text.strip():
            gettime = row.find("span",
                               {
                                   'id': re.compile(r'(MTG_SCHED\$)([0-9]{1})([0-9]{1})')  # noqa
                               }
                               )
        time = gettime.text
        # time is returned as a value of
        # DD<space>STARTTIME<AM/PM><space>-<space>ENDTIME<AM/PM>
        # removes space, removes DD,splits by -.
        # This forms a list in the format
        # [XXXXAM, YYYYAM]
        # Where x is start, y is end
        strippedtime = (time.strip()[2:]).split("-")
        time = (strippedtime[0]).strip() if type else (strippedtime[1]).strip()
        time = self.__format_time(time)
        return time

    """
        Concantates a 0 if time is < 7 chars.
        @params time, time to modify.
    """
    def __format_time(self, time):
        if len(time) < 7:
            time = "0"+time
        return time
