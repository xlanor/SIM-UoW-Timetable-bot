from bs4 import BeautifulSoup
from .login import SIMConnect
from Models.exceptions import *
from .RipperDecorators import RipperDecorators
import re
class OtherClass(SIMConnect):
    static_other_class_page = "https://simconnect1.simge.edu.sg:444/psc/csprd_2/EMPLOYEE/HRMS/c/SA_LEARNER_SERVICES.SM_LIST_OTHER_CLAS.GBL"
    def __init__(self, username, password):
        super(OtherClass, self).__init__(username, password)
    
    def get_timetable_page(self):
        login_ps = self.attempt_login()
        if self.is_logged_in(login_ps):
            self.driver.get(OtherClass.static_other_class_page)
            tt_ps = self.driver.page_source
            return tt_ps
        else:
            self.driver.close()
            raise UnableToLogin("Unable to login using given credentials")

    def execute(self):
        formatted_result = self.get_timetable_page()
        self.parse(formatted_result)
        self.driver.close()
    def parse(self,formatted_result):
        soup = BeautifulSoup(formatted_result,'html.parser')
        rows = soup.findAll('tr',{'id' :re.compile(r'(trSM_EVT_PRS_VW\$0_row)(\d{1,2}$)')})
        for row in rows:
            class_name_soup = row.find('span',{'id':re.compile(r'(^SM_EVT_PRS_VW_DESCR60\$)(\d{1,2}$)')})
            class_type_soup = row.find('span',{'id':re.compile(r'(^TYPE\$)(\d{1,2}$)')})
            class_start_time_soup = row.find('span',{'id':re.compile(r'(^START_TIME\$)(\d{1,2}$)')})
            class_end_time_soup = row.find('span',{'id':re.compile(r'(^END_TIME\$)(\d{1,2}$)')})
            class_loc_soup = row.find('span',{'id':re.compile(r'(^LOCATION\$)(\d{1,2}$)')})
            class_name = class_name_soup.text
            class_type = class_type_soup.text
            class_date = self.__get_date(class_start_time_soup.text)
            start_time = self.__get_time(class_start_time_soup.text)
            end_time = self.__get_time(class_end_time_soup.text)
            class_loc = class_loc_soup.text

            print("Name:{} Type:{} Date:{} Start:{} End:{} Location:{}".format(class_name,class_type,class_date,start_time,end_time,class_loc))

    def __get_date(self,class_time_soup_text):
        return class_time_soup_text.split(" ")[0]
    
    @RipperDecorators.format_time
    def __get_time(self,class_time_soup_text):
        return class_time_soup_text.split(" ")[1]

    def __dump_page_source(self,name):
        n = "{}.txt".format(name)
        with open(n,'w') as l:
            l.write(self.driver.page_source)
