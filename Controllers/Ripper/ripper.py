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
#   Factory method to return a ripper
##
from Models.exceptions import *
from Controllers.Ripper.login import SIMConnect
from Controllers.Ripper.timetable import RipTimeTable
from Controllers.Ripper.new_timetable import RipTimeTable as NewRip
from Controllers.Ripper.other import OtherClass
class RipperFactory():
    @staticmethod
    def get_ripper(method: str,username: str,password: str) -> SIMConnect :
        """
        Gets and initalizes an object for further operation
        @str method, type of method to use
        @str username, username to pass into the object
        @str password, decrypted password to pass into the object

        @return SIMConnect, inherited classes of SIMConnect to utilize polymorphism
        """
        if method == "Login":
            return SIMConnect(username,password)
        elif method == "Rip":
            return RipTimeTable(username,password)
        elif method == "Other":
            return OtherClass(username,password)
        elif method == "NewRip":
            return NewRip(username,password)
        else:
            raise InvalidRipException("Invalid rip method was selcted")