from .login import SIMConnect
from Models.exceptions import *
from Models.classes import IndividualClassStructure
from .RipperDecorators import RipperDecorators
from contextlib import closing
from bs4 import BeautifulSoup
import re

class RipTimeTable(SIMConnect):

    static_timetable_page = "https://simconnect1.simge.edu.sg:444/psc/csprd_2/EMPLOYEE/HRMS/c/SA_LEARNER_SERVICES.SSR_SSENRL_LIST.GBL"  # noqa
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

    def process_subject_divs(self,subjectdiv):
        class_name = None
        for div in subjectdiv:
            subject_title_soup = div.find("td",
                                   {
                                      'class': 'PAGROUPDIVIDER'
                                   }
                                   )
            class_name = subject_title_soup.text
            subject_rows = div.findAll('tr',{'id':re.compile(r'(^trCLASS_MTG_VW\$)(\d{1,3})(_row)(\d{1,3}$)')})
            for row in subject_rows:
                class_type_soup = row.find('span',{'id':re.compile(r'(^MTG_COMP\$)(\d{1,3}$)')})
                class_date_soup = row.find('span',{'id':re.compile(r'(^MTG_DATES\$)(\d{1,3}$)')})
                class_time_soup = row.find('span',{'id':re.compile(r'(^MTG_SCHED\$)(\d{1,3}$)')})
                class_loc_soup = row.find('span',{'id':re.compile(r'(^MTG_LOC\$)(\d{1,3}$)')})
                cn = self.__get_class_name(class_type_soup.text)
                class_type = cn if cn else class_type
                class_date = self.__get_class_date(class_date_soup.text)
                class_start_time = self.__get_time(class_time_soup.text,True)
                class_end_time = self.__get_time(class_time_soup.text,False)
                class_loc = class_loc_soup.text
                print("Name:{} Type: {} Date:{} Start:{} End:{} Location:{}".format(class_name,class_type,class_date,class_start_time,class_end_time,class_loc))


    def __get_class_name(self,class_name_soup_text):
        if class_name_soup_text.strip():
            return class_name_soup_text
        else: return None

    def __get_class_date(self,class_date_soup_text):
        return class_date_soup_text.split("-")[0].rstrip()

    @RipperDecorators.format_time
    def __get_time(self,class_time_soup_text,time_type):
        time = class_time_soup_text.strip()[2:].split("-")
        return time[0].strip() if time_type else time[1].strip()

    def get_timetable_page(self):
        login_ps = self.attempt_login()
        if self.is_logged_in(login_ps):
            self.driver.get(RipTimeTable.static_timetable_page)
            tt_ps = self.driver.page_source
            return tt_ps
        else:
            self.driver.close()
            raise UnableToLogin("Unable to login using given credentials")

    def parse_timetable_source(self,formatted_result):
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
        self.process_subject_divs(subjectdiv)
        class_type_dict = {}
        list_of_results = []

        
        self.driver.close()
        return list_of_results

    """
        An override method for the super class.
    """
    def execute(self):
        formatted_result = self.get_timetable_page()
        return self.parse_timetable_source(formatted_result)