
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
#   New Timetable ripper
##
from .login import SIMConnect
from Models.exceptions import *
from Models.classes import IndividualClassStructure
from .RipperDecorators import RipperDecorators
from contextlib import closing
from bs4 import BeautifulSoup
from bs4.element import ResultSet
from typing import Union,List
import re

class RipTimeTable(SIMConnect):

    static_timetable_page = "https://simconnect1.simge.edu.sg:444/psc/csprd_2/EMPLOYEE/HRMS/c/SA_LEARNER_SERVICES.SSR_SSENRL_LIST.GBL"  # noqa

    
    def __init__(self, username: str, password: str):
        """
        Constructor, calls superclass
        @str params username, the username of the client
        @str password, the decrypted password of the client
        """
        super(RipTimeTable, self).__init__(username, password)
   
    def navigate_to_latest_timetable(self, driver, latest_term: int) -> BeautifulSoup:
        """
        Navigates to the latest timetable in the event
        that there is more than 1 timetable.
        @params driver, an initalized selenium dirver
        @int latest_term, the latest term that you want to pull.
        @return soup, a formated beautiful soup object.
        """
        # constructing the latest term's id
        newid = f'SSR_DUMMY_RECV1$sels${latest_term}$$0'


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

    def process_subject_divs(self,subjectdiv: ResultSet, holding_list: List):
        """
        Processes subject div, performs regex queries to extract data, initalize a class structure, and 
        place the values into the structure

        @ResultSet subjectdiv, a BeautifulSoup result set of divs with subjects
        @List holding_list, a list to hold the objects
        """
        class_name = None
        for div in subjectdiv:
            subject_title_soup = div.find("td",
                                   {
                                      'class': 'PAGROUPDIVIDER'
                                   }
                                   )
            class_name = subject_title_soup.text
            subject_rows = div.findAll('tr',{'id':re.compile(r'(^trCLASS_MTG_VW\$)(\d{1,3})(_row)(\d{1,3}$)')})
            class_type = None
            for row in subject_rows:
                
                ic = IndividualClassStructure(class_name)
                class_type_soup = row.find('span',{'id':re.compile(r'(^MTG_COMP\$)(\d{1,3}$)')})

                class_date_soup = row.find('span',{'id':re.compile(r'(^MTG_DATES\$)(\d{1,3}$)')})
                class_time_soup = row.find('span',{'id':re.compile(r'(^MTG_SCHED\$)(\d{1,3}$)')})
                class_loc_soup = row.find('span',{'id':re.compile(r'(^MTG_LOC\$)(\d{1,3}$)')})

                cn = self.__get_class_name(class_type_soup.text)
                class_type = cn if cn else class_type
                ic.class_type = class_type
                ic.date = self.__get_class_date(class_date_soup.text)
                ic.start_time = self.__get_time(class_time_soup.text,True)
                ic.end_time = self.__get_time(class_time_soup.text,False)
                ic.location = class_loc_soup.text

                # adds the class to the list.
                holding_list.append(ic)

                #print(f"Name: {class_name} Type:{class_type} Date:{class_date} Start:{class_start_time} End:{class_end_time} Location:{class_loc}")


    def helper_methods(self,*args):
        """
        Helper method to test private methods.
        NOT.INTENDED.FOR.USE.IN.PRODUCTION!!!!!!!!!!!!!!!!
        """
        if method_to_call == "name":
            return self.__get_class_name(*args)
        elif method_to_call == "date":
            return self.__get_class_date(*args)
        elif method_to_call == "time":
            return self.__get_time(*args)

    def __get_class_name(self,class_name_soup_text: str) -> Union[str, None]:
        """
        Formats the class name.
        This ensures that the first row with the class name will return the class name
        While the remainder which do not have a class name will not set the class name
        Thus, ensuring that they reuse the class name.

        @str class_name_soup_text, the item within class_name <span>
        @return str, returns the class name if found
        @return None, returns None if class name is not found
        """
        if class_name_soup_text.strip():
            return class_name_soup_text
        else: return None


    def __get_class_date(self,class_date_soup_text: str) -> str:
        """
        Splits the date and returns the first half of the split
        Since both halves are identical.

        @str class_date_soup_text, the text within date <span>
        @return str, the split operation, returning the first half in the array.
        """
        return class_date_soup_text.split("-")[0].rstrip()

    @RipperDecorators.format_time
    def __get_time(self,class_time_soup_text: str,time_type: bool) -> str:
        """
        Splits the date and returns the first or the second half.

        @str class_time_soup_text, the text within <span>
        @bool time_type, true if start time, false if end time
        @return str, first half of the split if time_type is true
        @return str, second half of the split if time_type is false

        Wrapped by a decorator format_time, which takes the output and
        proceeds to modify the said output(prepends 0 in the case of 300), for example
        """
        time = class_time_soup_text.strip()[2:].split("-")
        return time[0].strip() if time_type else time[1].strip()

    def get_timetable_page(self) -> str:
        """
        Attempts to login to the SIMConnect website, before navigating to
        the timetable page (441) in order to scrape the timetable page

        In the event that it is not able to login, an exception is raised.

        @return str, the page source of the timetable page.
        """

        login_ps = self.attempt_login()
        if self.is_logged_in(login_ps):
            self.driver.get(RipTimeTable.static_timetable_page)
            tt_ps = self.driver.page_source
            return tt_ps
        else:
            self.driver.close()
            raise UnableToLogin("Unable to login using given credentials")

    def parse_timetable_source(self,formatted_result: str) -> List:
        """
        Parses the page source code.
        First, it loads into a bs4 object, so that we can
        then use regex to search for specific terms in order to 
        determine the values for the various classes.

        @str formatted_result, page source in string form
        @return list_of_results, returns a list of class objects.
        """
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

        list_of_results = []
        self.process_subject_divs(subjectdiv,list_of_results)

        
        self.driver.close()
        return list_of_results

    def execute(self) -> List:
        """
        An override method for the super class.
        @return a list of class objects
        """
        formatted_result = self.get_timetable_page()
        return self.parse_timetable_source(formatted_result)