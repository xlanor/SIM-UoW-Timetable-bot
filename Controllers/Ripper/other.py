from bs4 import BeautifulSoup
from .login import SIMConnect
from Models.exceptions import *
from .RipperDecorators import RipperDecorators
from Models.classes import IndividualClassStructure
from typing import List
import re

class OtherClass(SIMConnect):

    static_other_class_page = "https://simconnect1.simge.edu.sg:444/psc/csprd_2/EMPLOYEE/HRMS/c/SA_LEARNER_SERVICES.SM_LIST_OTHER_CLAS.GBL"

    def __init__(self, username: str, password: str):
        """
        Constructor, calls superclass
        @str params username, the username of the client
        @str password, the decrypted password of the client
        """
        super(OtherClass, self).__init__(username, password)


    def get_timetable_page(self) -> str:
        """
        Attempts to login to the SIMConnect website, before navigating to
        the Other classes page (441) in order to scrape the timetable there

        In the event that it is not able to login, an exception is raised.

        @return str, the page source of the timetable page.
        """

        login_ps = self.attempt_login()
        if self.is_logged_in(login_ps):
            self.driver.get(OtherClass.static_other_class_page)
            tt_ps = self.driver.page_source
            return tt_ps
        else:
            self.driver.close()
            raise UnableToLogin("Unable to login using given credentials")


    def execute(self) -> List:
        """
        An override method for the super class.
        @return a list of class objects
        """
        formatted_result = self.get_timetable_page()
        self.driver.close()
        return self.parse_timetable_source(formatted_result)


    def parse_timetable_source(self,formatted_result: str) -> List:
        """
        Executes regex queries to pull out the relevant data
        @str formatted_result, the page source
        @return list, a list of IndividualClassStructure objects.
        """
        soup = BeautifulSoup(formatted_result,'html.parser')
        rows = soup.findAll('tr',{'id' :re.compile(r'(trSM_EVT_PRS_VW\$0_row)(\d{1,2}$)')})
        holding_list = []
        for row in rows:
            class_name_soup = row.find('span',{'id':re.compile(r'(^SM_EVT_PRS_VW_DESCR60\$)(\d{1,2}$)')})
            class_type_soup = row.find('span',{'id':re.compile(r'(^TYPE\$)(\d{1,2}$)')})
            class_start_time_soup = row.find('span',{'id':re.compile(r'(^START_TIME\$)(\d{1,2}$)')})
            class_end_time_soup = row.find('span',{'id':re.compile(r'(^END_TIME\$)(\d{1,2}$)')})
            class_loc_soup = row.find('span',{'id':re.compile(r'(^LOCATION\$)(\d{1,2}$)')})
            ic = IndividualClassStructure(class_name_soup.text)
            ic.class_type = class_type_soup.text
            ic.date = self.__get_date(class_start_time_soup.text)
            ic.start_time = self.__get_time(class_start_time_soup.text)
            ic.end_time = self.__get_time(class_end_time_soup.text)
            ic.location = class_loc_soup.text
            holding_list.append(ic)
        return holding_list

    def __get_date(self,class_time_soup_text):
        return class_time_soup_text.split(" ")[0]
    
    @RipperDecorators.format_time
    def __get_time(self,class_time_soup_text):
        return class_time_soup_text.split(" ")[1]

    def __dump_page_source(self,name):
        n = "{}.txt".format(name)
        with open(n,'w') as l:
            l.write(self.driver.page_source)
