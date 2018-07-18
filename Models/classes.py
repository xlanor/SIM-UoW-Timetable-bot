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
from .exceptions import *

from typing import Dict, Union

class IndividualClassStructure():
    def __init__(self, name: str):
        self.__name = name
        # Initialize a few empty holding vars.
        self.__date = None
        self.__starttime = None
        self.__endtime = None
        self.__location = None
        self.__class_type = None

    def get_dict(self) -> Dict[str,str]:
        """
        Gets the variables in a dictionary format.
        @return dict
        """
        return_dict = {
                        "class_name": self.__name,
                        "date": self.__date,
                        "start_time": self.__starttime,
                        "end_time": self.__endtime,
                        "location": self.__location,
                        "type": self.__class_type
                        }
        return return_dict

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

    """
    A whole bunch of setter methods.
    """
    @name.setter
    def name(self,n: str) -> Union[str,None]:
        self.__name = n
    
    @date.setter
    def date(self,d: str) -> Union[str,None]:
        self.__date = d
    
    @start_time.setter
    def start_time(self,st: str) -> Union[str,None]:
        self.__starttime = st
    
    @end_time.setter
    def end_time(self, ed: str) -> Union[str,None]:
        self.__endtime = ed
    
    @location.setter
    def location(self,l: str) -> Union[str,None]:
        self.__location = l

    @class_type.setter
    def class_type(self,ct: str) -> Union[str,None]:
        self.__class_type = ct
