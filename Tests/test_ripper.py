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
#   Testing of the login function.
##
import pytest

from bs4 import BeautifulSoup
from Controllers.Ripper.login import SIMConnect
from Controllers.Ripper.new_timetable import RipTimeTable
from Controllers.Ripper.other import OtherClass
from Controllers.Ripper.ripper import RipperFactory
from Models.exceptions import *


pre_login_template = ""
with open("./Tests/page_sources/pre_login.log") as pre:
    s = pre.read()
    pre_login_template += s

post_login_template = ""
with open("./Tests/page_sources/post_login.log") as post:
    ps = post.read()
    post_login_template += ps

timetable_template = ""
with open("./Tests/page_sources/timetable_page_source.log") as tt:
    t = tt.read()
    timetable_template += t


# no proper way to test a login.
# we test for
# a) by instantiating a SIMConnect object, whether chromedriver is
#    properly installed and will launch properly.
# b) we pass in a mocked page source to determine if the logged in
#    detection works.
# Testing of SuperClass
def test_failed_logged_in():
    assert (
        SIMConnect("testing", "testing").is_logged_in(pre_login_template) is False
    ), "Failed Login Template test at SIMConnect Object failed!"


def test_logged_in():

    assert (
        SIMConnect("testing", "testing").is_logged_in(post_login_template) is True
    ), "Login Template test at SIMConnect Object failed!"


def test_fail_factory_method():
    try:
        # We DONT want to check subclass here, so we
        # opt for == over isinstance.
        rf = RipperFactory.get_ripper("garbage", "test", "test")
        pytest.fail("Garbage did not raise a InvalidRipException as expected")
    except InvalidRipException:
        assert True


def test_rip_factory_method():
    rf = RipperFactory.get_ripper("NewRip", "test", "test")
    assert type(rf) == RipTimeTable, "NewRip did not return an instance of RipTimeTable"


def test_other_factory_method():
    rf = RipperFactory.get_ripper("Other", "test", "test")
    assert type(rf) == OtherClass, "Other did not return an instance of OtherClass"


def test_login_factory_method():
    rf = RipperFactory.get_ripper("Login", "test", "test")
    assert type(rf) == SIMConnect, "Login did not return an instance of SIMConnect"
