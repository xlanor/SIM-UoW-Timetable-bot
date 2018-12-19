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
#   Login Method for SIMConnect.
##

# Default/Third Party Library imports
import time as clock
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys

# Internal project imports
from Models.exceptions import *


class SIMConnect:
    static_login_url = "https://simconnect.simge.edu.sg/psp/paprd/EMPLOYEE/HRMS/s/WEBLIB_EOPPB.ISCRIPT1.FieldFormula.Iscript_SM_Redirect?cmd=login"  # noqa
    static_logout_url = (
        "https://simconnect.simge.edu.sg/psp/paprd/EMPLOYEE/EMPL/?cmd=logout"
    )  # noqa

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.__chrome_driver = None
        self.driver = None
        self.__loadDriver()

    def __loadDriver(self):
        capabilities = webdriver.DesiredCapabilities().CHROME.copy()
        capabilities["acceptInsecureCerts"] = True
        self.driver = webdriver.Chrome(
            options=self.__chrome_options(),
            service_args=["--verbose", "--log-path=./chromedriver.log"],
            desired_capabilities=capabilities,
            executable_path="./chromedriver",
        )  # noqa

    def __chrome_options(self):
        # instantiate a chrome options object so you can set the size and headless preference
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--window-size=1124x850")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--test-type")
        return chrome_options

    def attempt_login(self):
        print("Attempting login for {}".format(self.username))
        self.driver.get(SIMConnect.static_login_url)
        # we use sleep to let the page happily load throughout the script.
        clock.sleep(6)
        self.driver.save_screenshot("login_page.png")
        selection = self.driver.find_element_by_xpath(
            "//select[@id='User_Type']/option[@value='Student']"
        ).click()

        clock.sleep(5)
        # finds userinput box
        usr = self.driver.find_element_by_name("userid")
        # finds password box
        passw = self.driver.find_element_by_name("pwd")
        # finds login button
        logbtn = self.driver.find_element_by_name("Submit")
        # sends the keys to the driver
        usr.send_keys(self.username)
        passw.send_keys(self.password)
        # clicks the button
        logbtn.click()
        clock.sleep(6)
        self.driver.save_screenshot("test.png")
        return self.driver.page_source

    def __dump_page_source(self, name):
        n = "{}.txt".format(name)
        with open(n, "w") as l:
            l.write(self.driver.page_source)

    """
    The reason why we partition this seperately and have a sep main function is so that we can
    write a unit test for it to pass in a page source.
    """

    def is_logged_in(self, page_source):
        if SIMConnect.static_logout_url in page_source:
            print("Logged in for {}".format(self.username))
            return True
        else:
            print("Failed login for {}".format(self.username))
            return False

    """
    Execution method
    """

    def execute(self):
        page_source = self.attempt_login()
        ps = self.is_logged_in(page_source)
        self.driver.quit()
        return ps
