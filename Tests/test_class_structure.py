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
#   Testing of the regex methods in the class structure
#   Written by xlanor
##

from bs4 import BeautifulSoup
from Models.classes import IndividualClassStructure
import pytest
from Models.exceptions import *

# SINGLE ROW HTML BEGINS HERE
single_row_date = """<div id="win2divMTG_DATES$6"><span class="PSEDITBOX_DISPONLY" id="MTG_DATES$6">05/07/2018 - 05/07/2018</span>"""
single_row_time = """<div id="win2divMTG_SCHED$6"><span class="PSEDITBOX_DISPONLY" id="MTG_SCHED$6">Th 8:30AM - 11:30AM</span>"""
single_row_loc="""<div id="win2divMTG_LOC$6"><span class="PSEDITBOX_DISPONLY" id="MTG_LOC$6">HQ BLK B LT B.4.17</span>"""

# DOUBLE ROW HTML BEGINS HERE
double_row_date = """<div id="win2divMTG_DATES$16"><span class="PSEDITBOX_DISPONLY" id="MTG_DATES$16">05/07/2018 - 05/07/2018</span>"""
double_row_time = """<div id="win2divMTG_SCHED$16"><span class="PSEDITBOX_DISPONLY" id="MTG_SCHED$16">Th 8:30AM - 11:30AM</span>"""
double_row_loc="""<div id="win2divMTG_LOC$16"><span class="PSEDITBOX_DISPONLY" id="MTG_LOC$16">HQ BLK B LT B.4.17</span>"""


# FAILING HTML BEGINS HERE
single_fail_row_date = """<div id="win2divMTG_FAILS$6"><span class="PSEDITBOX_DISPONLY" id="MTG_FAILS$6">05/07/2018 - 05/07/2018</span>"""
double_fail_row_date = """<div id="win2divMTG_FAILS$16"><span class="PSEDITBOX_DISPONLY" id="MTG_FAILS$16">05/07/2018 - 05/07/2018</span>"""

"""
LIST
[15, 25]
CLASS
{25: 'Tutorial', 15: 'Lecture'}
KEYS
2
ROWID
29
"""

single_digit_row = IndividualClassStructure("Test")
double_digit_row = IndividualClassStructure("TestDoubleDigit")
def test_class_date():
    # Test single digit rows
    single_digit_row.set_date_of_class(load_soup(single_row_date))
    assert single_digit_row.get_date() == "05/07/2018", "Single Row Date Failed"
    double_digit_row.set_date_of_class(load_soup(double_row_date))
    assert double_digit_row.get_date() == "05/07/2018", "Double Row Date Failed"

def test_load_class_time():
    single_digit_row.set_time(True,load_soup(single_row_time))
    single_digit_row.set_time(False,load_soup(single_row_time))
    assert single_digit_row.get_start_time() is not None, "Single Row Start Time Failed"
    double_digit_row.set_time(True,load_soup(double_row_time))
    double_digit_row.set_time(False,load_soup(double_row_time))
    assert double_digit_row.get_start_time() is not None, "Double Row Start Time Failed"

def test_parse_class_time():
    assert single_digit_row.get_start_time() == "05/07/2018 08:30AM", "Single Row Start Time Inaccurate"
    assert single_digit_row.get_end_time() == "05/07/2018 11:30AM", "Single Row End Time Inaccurate"
    assert double_digit_row.get_start_time() == "05/07/2018 08:30AM", "Double Row Start Time Inaccurate"
    assert double_digit_row.get_end_time() == "05/07/2018 11:30AM", "Double Row End Time Inaccurate"

def test_loc():
    single_digit_row.set_location(load_soup(single_row_loc))
    double_digit_row.set_location(load_soup(double_row_loc))
    assert single_digit_row.get_loc() == "HQ BLK B LT B.4.17", "Single Row Location Failed"
    assert double_digit_row.get_loc()  == "HQ BLK B LT B.4.17", "Double Row Location Failed"

list_of_class_type_keys = [15, 25]
class_type_dict = {25: 'Tutorial', 15: 'Lecture'}
no_of_keys = 2
actual_row_id = 29

def test_class_type():
    # row doesnt matter.
    # we use single digit to test.
    actual_row_id = 16
    #with pytest.raises(RegexNotFound):
    single_digit_row.determine_class_type(list_of_class_type_keys,class_type_dict,no_of_keys,actual_row_id)
    assert single_digit_row.get_class_type() == "Lecture", "Location algorithm failed"
    actual_row_id = 29
    single_digit_row.determine_class_type(list_of_class_type_keys,class_type_dict,no_of_keys,actual_row_id)
    assert single_digit_row.get_class_type() == "Tutorial", "Location algorithm failed"
    try:
        actual_row_id = 2
        single_digit_row.determine_class_type(list_of_class_type_keys,class_type_dict,no_of_keys,actual_row_id)
        pytest.fail("Regex not found supposed to be raised")
    except RegexNotFound:
        pas
    


single_digit_failing_row = IndividualClassStructure("Test")
double_digit_failing_row = IndividualClassStructure("TestDoubleDigit")
def test_failing_html():
    with pytest.raises(RegexNotFound):
        single_digit_failing_row.set_date_of_class(load_soup(single_fail_row_date))
        double_digit_failing_row.set_date_of_class(load_soup(double_fail_row_date))
        # we can just use the date for time since we're testing regex for MTG_SCHED
        single_digit_failing_row.set_time(True,load_soup(single_fail_row_date))
        double_digit_failing_row.set_time(True,load_soup(double_fail_row_date))
        single_digit_failing_row.set_location(load_soup(single_fail_row_date))
        double_digit_failing_row.set_location(load_soup(double_fail_row_date))




def load_soup(soup_to_load):
    return BeautifulSoup(soup_to_load,'html.parser')
    