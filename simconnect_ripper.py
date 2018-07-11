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
#   Cronus module to rip the timetable from SIM connect
#   Using PhantomJS as a headless browser, and selenium or
#   bs4 to navigate and scrape the results.
##
import time as clock
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from contextlib import closing
from bs4 import BeautifulSoup
import re
import json
import sys
from Models.classes import IndividualClassStructure
from Models.attendance import Attendance

"""
    Superclass definition.
"""


class SIMConnect():
    """
        Constructor
        @params username, the username of the client
        @params password, the decrypted password of the client
    """
    def __init__(self, username, password):
        # noqa is used here to prevent breaking of PEP-8
        self.__login_url = "https://simconnect.simge.edu.sg/psp/paprd/EMPLOYEE/HRMS/s/WEBLIB_EOPPB.ISCRIPT1.FieldFormula.Iscript_SM_Redirect?cmd=login"  # noqa
        self.timetable_page = "https://simconnect1.simge.edu.sg:444/psc/csprd_2/EMPLOYEE/HRMS/c/SA_LEARNER_SERVICES.SSR_SSENRL_LIST.GBL"  # noqa
        self.logout_url = "https://simconnect.simge.edu.sg/psp/paprd/EMPLOYEE/EMPL/?cmd=logout"  # noqa
        self.username = username
        self.password = password
        #self.driver = webdriver.PhantomJS(executable_path='./phantomjs', service_args=['--ignore-ssl-errors=true', '--ssl-protocol=TLSv1'])  # noqa
        self.__chrome_driver = None
        self.driver = None
        self.__loadDriver()
    
    def __loadDriver(self):
        capabilities = webdriver.DesiredCapabilities().CHROME.copy()
        capabilities['acceptInsecureCerts'] = True
        self.driver = webdriver.Chrome(chrome_options=self.__chrome_options(),service_args=["--verbose", "--log-path=./chromedriver.log"],desired_capabilities=capabilities, executable_path="./chromedriver")


    def __chrome_options(self):
        # instantiate a chrome options object so you can set the size and headless preference
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--window-size=1124x850")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--test-type")
        return chrome_options
    """
        Login method to spoof a login by phantomJS
        @return string, the whole page source.
    """   
    def login(self):
        self.driver.get(self.__login_url)
        # we use sleep to let the page happily load throughout the script.
        clock.sleep(6)
        self.driver.save_screenshot('login_page.png')
        selection = self.driver.find_element_by_xpath("//select[@id='User_Type']/option[@value='Student']").click()

        clock.sleep(5)
        # finds userinput box
        usr = self.driver.find_element_by_name('userid')
        # finds password box
        passw = self.driver.find_element_by_name('pwd')
        # finds login button
        logbtn = self.driver.find_element_by_name('Submit')
        # sends the keys to the driver
        usr.send_keys(self.username)
        passw.send_keys(self.password)
        # clicks the button
        logbtn.click()
        clock.sleep(6)
        # print (driver.page_source)
        self.driver.save_screenshot('test.png')
        return self.driver.page_source
    """
        Default execution method that checks for login
        @return boolean variable , True if able to login else false.
    """
    def execute(self):
        # "API" that populates timetable. It was never designed
        # for this purpose, but we're going to use it
        # initialize PhantomJS, define settings
        page_source = self.login()
        if self.logout_url in page_source:
            self.driver.close()
            return True
        else:
            self.driver.close()
            return False
"""
    RipTimeTable inherits SIMConnect.
"""


class RipTimeTable(SIMConnect):
    """
        Constructor, calls superclass
        @params username, the username of the client
        @params password, the decrypted password of the client
    """
    def __init__(self, username, password):
        super(RipTimeTable, self).__init__(username, password)
    """
        Navigates to the latest timetable in the event
        that there is more than 1 timetable.
        @params driver, an initalized selenium dirver
        @params latest_term, the latest term that you want to pull.
        @return soup, a formated beautiful soup object.
    """
    def navigate_to_latest_timetable(self, driver, latest_term):
        # constructing the latest term's id
        newid = 'SSR_DUMMY_RECV1$sels$'+str(latest_term)+'$$0'

        # using selenium to hunt for the element and click
        term_button = driver.find_element_by_id(newid)
        term_button.click()

        # more hunting for buttons.
        continue_button = driver.find_element_by_id(
                                                    'DERIVED_SSS_SCT_SSR_PB_GO'
                                                    )
        continue_button.click()

        # loading the new timetablepage...
        clock.sleep(5)

        # grab the source, format it, return to bs4
        new_formatted_result = driver.page_source
        soup = BeautifulSoup(new_formatted_result, "html.parser")

        return soup

    """
        Sort the type of classes.
        @params row, a row pulled from the thml
        @params class_type_dict, the dictionary to store the class type.
    """
    def __type_of_classes(self, row, class_type_dict):
        gettype = row.find("span",
                           {
                                "id": re.compile(r'(MTG_COMP\$)([0-9]{1})')
                           }
                           )
        if not gettype.text:
            gettype = row.find("span",
                               {
                                   "id": re.compile(r'(MTG_COMP\$)([0-9]{1})([0-9]{1})')  # noqa
                               }
                               )

        if gettype.text.strip():
            type_class = gettype.text
            type_id = int((((gettype.get('id')).split("$"))[1]).strip())
            '''#########################################################
                        Only the first row for each type has
                            the value of the type.
                    ie: row 0, first lecture type will contain
                lecture., then its blank until row 15, row 15 contains
                tutorial. We put it into a dict to compare later.
            #########################################################'''
            class_type_dict[type_id] = type_class

    """
        Gets the row id for further usage
        @params row, a row pulled from the HTML
        @return rowid, the current row id.
    """
    def __get_row_id(self, row):
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

        rowid = (((getlocation.get('id')).split("$"))[1]).strip()
        return rowid

    def handle_single_digit_row(self, singledigittablerow,
                                class_type_dict, list_of_results,
                                subjectitlename):
        for row in singledigittablerow:
            # Instantiate a  new class object.
            class_object = IndividualClassStructure(subjectitlename)
            '''####################################################################################
                                    Here we're going to use regex.
                              Why do we repeat same regex twice with variance?
                            First we check for id with regex for single digit
                                     For example, MTG_DATES$0
                                  If in that div, MTGDATES$# WHERE # is a
                                    random number does not match regex,
                                    It means that we're in a row where
                                        MTGDATES$ is MTGDATES$##
                                Thus we write another regex for that row.
                                  This was probably never meant to be
                              pulled as an API that's why its so fucked up.
            ####################################################################################'''  # noqa

            self.__type_of_classes(row, class_type_dict)

            # Sets the date of the class in the class object.
            class_object.set_date_of_class(row)
            # Sets the start time of the class
            class_object.set_time(True, row)
            # Sets the end time of the class
            class_object.set_time(False, row)
            # Sets the location of the class (where the class is being held.)
            class_object.set_location(row)
            # Time to determine class type from the array above.
            rowid = self.__get_row_id(row)
            list_of_class_type_keys = list(class_type_dict.keys())
            list_of_class_type_keys = sorted(list_of_class_type_keys)
            no_of_keys = len(list_of_class_type_keys)

            class_object.determine_class_type(list_of_class_type_keys,
                                              class_type_dict, no_of_keys,
                                              rowid
                                              )

            list_of_results.append(class_object)
    """
        process the subject div.
        @ params subjectdiv, a div of subjects extracted from the html.
        @ params class_type_dict, an empty dictionary.
        @ params list_of_results, an empty list.
    """
    def process_subject_div(self, subjectdiv,
                            class_type_dict, list_of_results):
        for div in subjectdiv:
            class_type_dict.clear()
            subjectitle = div.find("td",
                                   {
                                      'class': 'PAGROUPDIVIDER'
                                   }
                                   )
            subjectitlename = subjectitle.text
            singledigittablerow = div.findAll('tr',
                                                {
                                                    'id': re.compile(r'(trCLASS_MTG_VW\$)([0-9]{1})(_row)([0-9]{1})')  # noqa
                                                }
                                                )
            self.handle_single_digit_row(singledigittablerow,
                                         class_type_dict, list_of_results,
                                         subjectitlename
                                         )
    """
        An override method for the super class.
    """
    def execute(self):
        # "API" that populates timetable.
        # It was never designed for this purpose,
        # but we're going to use it
        # initialize PhantomJS, define settings
        page_source = self.login()
        if self.logout_url in page_source:
            self.driver.get(self.timetable_page)
            formatted_result = self.driver.page_source
            soup = BeautifulSoup(formatted_result, "html.parser")
            termdiv = soup.findAll('span',
                                   {
                                       'id': re.compile(r'(TERM_CAR\$)([0-9]{1})')  # noqa
                                   }
                                   )

            # If there is more than 1 timetable avaliable,
            # we default to the latest term's timetable.
            if len(termdiv) != 0:
                latest_term = len(termdiv)-1
                soup = self.navigate_to_latest_timetable(self.driver, latest_term)

            # list of all the subjects.
            subjectdiv = soup.findAll('div',
                                      {
                                          'id': re.compile(r'(win2divDERIVED_REGFRM1_DESCR20\$)([0-9]{1})')  # noqa
                                      }
                                      )
            class_type_dict = {}
            list_of_results = []

            self.process_subject_div(subjectdiv, class_type_dict,
                                     list_of_results)
            self.driver.close()
            return(list_of_results)
        else:
            self.driver.close()
            return []
"""
    Not really necessary, but I dont like calling a superclass blindly.
    Inherits from SIMConnect superclass.
"""


class LoginTest(SIMConnect):
    def __init__(self, username, password):
        super(LoginTest, self).__init__(username, password)

"""
    Attendence inherits SIMConnect superclass
"""


class Attendance(SIMConnect):
    def __init__(self, username, password):
        super(Attendance, self).__init__(username, password)
        self.__student_center_url = 'https://simconnect.simge.edu.sg/psp/paprd_2/EMPLOYEE/HRMS/c/SA_LEARNER_SERVICES.SSS_STUDENT_CENTER.GBL'  # noqa
        self.__attendance_selection_id = '4030'  #4030 is the value of the attendence selection.

    def checkatt(self):
        page_source = self.login()
        if self.logout_url in page_source:
            return self.__navigate_attendance()
        else:
            return []

    def __navigate_attendance(self):
        self.driver.get(self.__student_center_url)
        clock.sleep(10)

        # find the iframe
        frame = self.driver.find_element_by_id("ptifrmtgtframe")
        # switch to iframe.
        self.driver.switch_to.frame(frame)
        #at student center page, click drop down
        select = Select(self.driver.find_element_by_id("DERIVED_SSS_SCL_SSS_MORE_ACADEMICS"))
        select.select_by_value(self.__attendance_selection_id)
        clock.sleep(10)
        gobtn = self.driver.find_element_by_id('DERIVED_SSS_SCL_SSS_GO_1')
        gobtn.click()
        clock.sleep(10)
        # formatted_result = self.driver.page_source
        # soup = BeautifulSoup(formatted_result,"html.parser")
        formatted_result = self.driver.page_source
        att = Attendance(formatted_result)

        if not self.__get_attendance(att):
            print ("float conversion error")
        return att


    def __get_attendance(self,att_obj):
        try:
            att = float(att_obj.getPartner())
        except ValueError:
            return False
        else:  # win2divCLASSES$0
            if float(att) != 100.00:
                formatted_result = self.driver.page_source
                soup = BeautifulSoup(formatted_result,"html.parser")
                classes = soup.findAll('span',
                                       {
                                           'id': re.compile(r'(CLASSES\$span\$)([0-9]{1})')  # noqa
                                       }
                                       )
                lastindex = len(classes)-1
                while lastindex >= 0:
                    self.navigate_classes(attobj,lastindex)
                    lastindex -= 1

            return True

    def navigate_classes(self,returndict,index):
        classid = "SM_STDNT_CLASS$sels$"+str(index)+"$$0"
        classbtn =  self.driver.find_element_by_id(classid)
        classbtn.click()
        continuebtn = self.driver.find_element_by_id("SM_CUSTOM_WRK_SSR_PB_GO")
        continuebtn.click()
        clock.sleep(10)
        #we are now in the class. lets find the attendance.
        no_classes = self.getnoclasses()
        counter = 0
        while counter < no_classes:
            attid = "SM_CUSTOM_WRK_SM_ATTEND_PRESENT$"+str(counter)
            attdateid = "SM_CLS_ATND_VW4_CLASS_ATTEND_DT$"+str(counter)
            attstarttime = "SM_CLS_ATND_VW4_ATTEND_FROM_TIME$"+str(counter)
            present = self.driver.find_element_by_id(attid)
            if present.text == "No":
                #SM_CLS_ATND_VW4_CLASS_ATTEND_DT$
                class_name = self.driver.find_element_by_id("DERIVED_SSR_FC_SSR_CLASSNAME_LONG$span").text
                date_of_absence = self.driver.find_element_by_id(attdateid).text
                start_time = self.driver.find_element_by_id(attstarttime).text
                returndict['Absent'].append({"name":class_name,"date":date_of_absence,"time":start_time})
            counter +=1

        backtbtn = self.driver.find_element_by_id("SM_CUSTOM_WRK_SSS_CHG_CLS_LINK")
        backtbtn.click()
        clock.sleep(10)

    def getnoclasses(self):
        total_class = 0
        formatted_result = self.driver.page_source
        soup = BeautifulSoup(formatted_result,"html.parser")

        no_classes = soup.findAll('span',{'id':re.compile(r'(SM_CLS_ATND_VW4_CLASS_ATTEND_DT\$)([0-9]{1})')})
        if len(no_classes) > 0:
            no_classes_2 = soup.find("span",{"id":re.compile(r'(SM_CLS_ATND_VW4_CLASS_ATTEND_DT\$)([0-9]{1})([0-9]{1})')})

        try:
            total_class += len(no_classes)
        except TypeError:
            pass
        except ValueError:
            pass
                    
        try:
            total_class += len(no_classes_2)
        except TypeError:
            pass
        except ValueError:
            pass

        return total_class
"""
    For testing purposes only.
"""
if __name__ == "__main__":
    # Loads an account from testing_accounts.json which is
    # placed in .gitignore to ensure that we don't accidentally
    # commit our tester accounts to git.
    # Big thanks to Ray Keeve from UOB and See Yi Ze from UOL
    # for volunteering to be guinea pigs. If you would like to
    # be a guinea pig for this project, drop me a mail at contact@jingk.ai
    """
    JSON Format
            {
            "ray":{
                    "username": <String>,
                    "password":<String>
                },
            "jk":{
                    "username":<String>,
                    "password":<String>"

                },
            "yz":{
                    "username":<String>,
                    "password":<String>
                }
            }
    """
    user_to_load = input("Enter a user to load: (ray|jk|yz) : ")
    with open("testing_accounts.json") as json_file:
        data = json.load(json_file)
        try:
            data[user_to_load]
        except KeyError:
            print("Cannot find data in file")
            sys.exit()
        else:
            username = data[user_to_load]["username"]
            password = data[user_to_load]["password"]
            method = input("What type of test would you like to perform? (rip | login): ")  # noqa
            if method == "rip":
                list_of_classes = (RipTimeTable(username, password).execute())
                for cl in list_of_classes:
                    print(cl.get_dict())
            elif method == "login":
                print(LoginTest(username, password).execute())
            else:
                print("Unknown method")
