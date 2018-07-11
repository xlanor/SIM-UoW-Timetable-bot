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
#   Model to hold attendance information
#   Written by xlanor
##

from bs4 import BeautifulSoup
from .classes import IndividualClassStructure

class Attendance():
    def __init__(self,page_source):
        self.__formatted = BeautifulSoup(page_source,"html.parser")
        icaspan = self.__formatted.find('span',
                                        {'id': 'SM_CUSTOM_WRK_DESCR50$0'
                                        }
                                        )
        simglobalspan = self.__formatted.find('span',
                                              {'id': 'SM_CUSTOM_WRK_DESCR50$1'
                                              }
                                              )
        partnerspan = self.__formatted.find('span',
                                            {'id': 'SM_CUSTOM_WRK_DESCR50$2'
                                            }
                                            )
        uniname = self.__formatted.find('span',
                                        {'id': 'INSTITUTION_TBL_DESCR'
                                        }
                                        )
        termname = self.__formatted.find('span',
                                        {'id': 'TERM_TBL_DESCR'
                                        }
                                        )
        programname = self.__formatted.find('span',
                                            {'id': 'SM_STUDENT_TERM_DESCR'
                                            }
                                            )

        self.__ICA  = icaspan.text if icaspan else "N/A"
        self.__SIM = simglobalspan.text if simglobalspan else "N/A"
        self.__partner = partnerspan.text
        self.__uni_name = uniname.text
        self.__term = termname.text
        self.__prog = programname.text
        self.__absent = []
    
    @property
    def getICA(self):
        return self.__ICA
    
    @property
    def getSIM(self):
        return self.__SIM

    @property
    def getPartner(self):
        return self.__partner
    
    @property
    def getUni(self):
        return self.__uni_name

    @property
    def getTerm(self):
        return self.__term
    
    @property
    def getProg(self):
        return self.__prog

    @property
    def getAbsent(self):
        return self.__absent

    def addAbsent(self,absent_class_obj):
        self.__absent.append(absent_class_obj)
    

class AbsentClasses():
    def __init__(self,name,date,time):
        self.__name = name
        self.__date = date
        self.__time = time
    
    @property
    def getName(self):
        return self.__name
    
    @property
    def getDate(self):
        return self.__date
    
    @property
    def getTime(self):
        return self.__time

