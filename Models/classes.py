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
#   Model to hold data from a Class retrieved via scraping
##

# Native/3rd party imports.
import time as clock
import re
from bs4 import BeautifulSoup
from datetime import datetime
from typing import Dict, Union
import calendar


# Local imports
from .exceptions import *


class IndividualClassStructure():
    def __init__(self, name: str):
        self.__name = name
        # Initialize a few empty holding vars.
        self.__date = None
        self.__starttime = None
        self.__endtime = None
        self.__location = None
        self.__class_type = None
        self.__class_day = None
        self.__class_numeric_day = None

    def get_dict(self) -> Dict[str,str]:
        """
        Gets the variables in a dictionary format.
        @return dict
        """
        #self.get_date_text_index()
        return_dict = {
                        "class_name": self.__name,
                        "date": self.__date,
                        "day": self.__class_day,
                        "numeric_day" : self.__class_numeric_day,
                        "start_time": self.__starttime,
                        "end_time": self.__endtime,
                        "location": self.__location,
                        "type": self.__class_type,
                        }
        return return_dict

    def get_dict_mongo(self) -> Dict[str,str]:
        self.get_date_text_index()
        start_time_w_date = f"{self.__date} {self.__starttime}"
        end_time_w_date = f"{self.__date} {self.__endtime}"
        return_dict = {
                            "class_name": self.__name,
                            "date": datetime.strptime(self.__date, '%d/%m/%Y'),
                            "day": self.__class_day,
                            "numeric_day" : self.__class_numeric_day,
                            "start_time": datetime.strptime(start_time_w_date, '%d/%m/%Y %I:%M%p'),
                            "end_time": datetime.strptime(end_time_w_date , '%d/%m/%Y %I:%M%p'),
                            "location": self.__location,
                            "type": self.__class_type
                        }
        return return_dict
    
    def get_formatted_text(self):
        # this is assuming the dates stored here are in
        # DATE TIME OBJECT NOT STRING.
        # markdown syntax.
        class_text = []
        class_text.append(f"📌 _{self.__name}_\n")
        class_text.append("```\n")
        class_text.append(f"Date: {datetime.strftime(self.__date,'%b %d %Y')}\n")
        class_text.append(f"Type: {self.__class_type}\n")
        class_text.append(f"Start Time: {datetime.strftime(self.__starttime,'%H:%M')}\n")
        class_text.append(f"End Time: {datetime.strftime(self.__endtime,'%H:%M')}\n")
        class_text.append(f"Location: {self.__location}\n")
        class_text.append(f"```")
        return "".join(class_text)
    
    """
    A whole bunch of getter methods.
    """
    @property
    def name(self):
        return self.__name
    
    @property
    def date(self):
        return self.__date
    
    @property
    def start_time(self):
        return self.__starttime
    
    @property
    def end_time(self):
        return self.__endtime
    
    @property
    def location(self):
        return self.__location
    
    @property
    def class_type(self):
        return self.__class_type
    
    @property
    def class_day(self):
        return self.__class_day
    
    @property
    def class_numeric_day(self):
        return self.__class_numeric_day
    """
    A whole bunch of setter methods.
    """
    @name.setter
    def name(self,n: str):
        self.__name = n
    
    @date.setter
    def date(self,d: str):
        self.__date = d
    
    @start_time.setter
    def start_time(self,st: str):
        self.__starttime = st
    
    @end_time.setter
    def end_time(self, ed: str):
        self.__endtime = ed
    
    @location.setter
    def location(self,l: str):
        self.__location = l

    @class_type.setter
    def class_type(self,ct: str) -> Union[str,None]:
        self.__class_type = ct
        
    def get_date_text_index(self):
        date = datetime.strptime(self.__date, '%d/%m/%Y')
        numeric_day = date.weekday()
        string_day = calendar.day_name[numeric_day]
        self.__class_numeric_day = numeric_day
        self.__class_day = string_day

    def set_from_dict(self,class_object_dict:Dict):
        """
        self.__name = name
        # Initialize a few empty holding vars.
        self.__date = None
        self.__starttime = None
        self.__endtime = None
        self.__location = None
        self.__class_type = None
        self.__class_day = None
        self.__class_numeric_day = None
        WHENEVER YOU POPULATE WITH THIS METHOD YOU MUST USE 
        "get_dict" instead of "get_dict_mongo" to retrieve the dict.
        """
        self.__name = class_object_dict["class_name"]
        # this should be an iso datetime obj. 
        self.__date = class_object_dict["date"]
        self.__class_day = class_object_dict["day"]
        self.__class_numeric_day = class_object_dict["numeric_day"]
        # this should be an iso datetime object
        self.__starttime = class_object_dict["start_time"]
        self.__endtime = class_object_dict["end_time"]
        self.__location = class_object_dict["location"]
        self.__class_type = class_object_dict["type"]