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
#   Testing of the timetable ripper.
##
from bs4 import BeautifulSoup
from Controllers.Ripper.new_timetable import RipTimeTable as rt
from Controllers.Ripper.other import OtherClass as other_class

timetable_template = ""
other_template = ""

r = rt("testing","testing")
o = other_class("testing","testing")
with open('./Tests/page_sources/timetable_page_source.log') as tt:
    t = tt.read()
    timetable_template += t
with open('./Tests/page_sources/other_tt.log') as ot:
    o_t = ot.read()
    other_template += o_t

def test_timetable_parser():
    list_of_class = r.parse_timetable_source(timetable_template)
    assert len(list_of_class) == 30, f'Expected 30 classes!'
    for c in list_of_class:
        assert c.name is not None, f'A retrived class has a null name'
        assert c.class_type is not None, f'A retrived class, {c.name} has a null class type'
        assert c.start_time is not None, f'A retrieved class, {c.name} has a null start_time'
        assert c.end_time is not None, f'A retrieved class, {c.name} has a null end time'
        # All time should be formatted as
        # 03:00PM | 12:30AM
        assert len(c.start_time) == 7, f'Class {c.name} of type {c.type} has a start time of an invalid length!'  
        assert len(c.end_time) == 7, f'Class {c.name} of type {c.type} has an end time of an invalid length!'

def test_other_parser():
    list_of_class = o.parse_timetable_source(other_template)
    assert len(list_of_class) == 23, f'Expected 23 classes!'
    for c in list_of_class:
        assert c.name is not None, f'A retrived class has a null name'
        assert c.class_type is not None, f'A retrived class, {c.name} has a null class type'
        assert c.start_time is not None, f'A retrieved class, {c.name} has a null start_time'
        assert c.end_time is not None, f'A retrieved class, {c.name} has a null end time'
        # All time should be formatted as
        # 03:00PM | 12:30AM
        assert len(c.start_time) == 7, f'Class {c.name} of type {c.type} has a start time of an invalid length!'  
        assert len(c.end_time) == 7, f'Class {c.name} of type {c.type} has an end time of an invalid length!'




