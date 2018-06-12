#! /usr/bin/env python3
#-*- coding: utf-8 -*-
##
# Cronus module to rip the timetable from SIM connect
# Using PhantomJS as a headless browser, and selenium | bs4 to navigate and scrape the results.
# Written by xlanor
##
import time as clock
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from contextlib import closing
from bs4 import BeautifulSoup
import re, json,sys
from Models.classes import IndividualClassStructure

"""
    Superclass definition.
"""
class SIMConnect():
    def __init__(self,username,password):
        self.__login_url = "https://simconnect.simge.edu.sg/psp/paprd/EMPLOYEE/HRMS/s/WEBLIB_EOPPB.ISCRIPT1.FieldFormula.Iscript_SM_Redirect?cmd=login"
        self.timetable_page = "https://simconnect1.simge.edu.sg:444/psc/csprd_2/EMPLOYEE/HRMS/c/SA_LEARNER_SERVICES.SSR_SSENRL_LIST.GBL"
        self.logout_url = "https://simconnect.simge.edu.sg/psp/paprd/EMPLOYEE/EMPL/?cmd=logout"
        self.username = username
        self.password = password
    """
        Login method to spoof a login by phantomJS
        @params username, the username of the client
        @params password, the decrypted password of the client
        @params driver, an initalized selenium driver.
    """
    def login(self,driver):
        
        driver.get(self.__login_url)
        # we use sleep to let the page happily load throughout the script.
        clock.sleep(5) 
        # finds userinput box
        usr = driver.find_element_by_name('userid')
        # finds password box
        passw = driver.find_element_by_name('pwd')
        # finds login button
        logbtn = driver.find_element_by_name('Submit') 
        # sends the keys to the driver
        usr.send_keys(self.username)
        passw.send_keys(self.password)
        #clicks the button
        logbtn.click()
        clock.sleep(6)
        #print (driver.page_source)
        driver.save_screenshot('test.png')
        return driver.page_source
    """ 
        Default execution method that checks for login 
    """
    def execute(self):
        #"API" that populates timetable. It was never designed for this purpose, but we're going to use it
        #initialize PhantomJS, define settings
        driver = webdriver.PhantomJS(executable_path='./phantomjs',service_args=['--ignore-ssl-errors=true', '--ssl-protocol=TLSv1'])
        driver.set_window_size(1124, 850) 
        page_source = self.login(driver)
        if self.logout_url in page_source:
            driver.close()
            return True
        else:
            driver.close()
            return False
"""
    RipTimeTable inherits SIMConnect.
"""
class RipTimeTable(SIMConnect):
    def __init__(self,username,password):
        super(RipTimeTable, self).__init__(username,password)
    """
        Navigates to the latest timetable in the event that there is more than 1 timetable.
        @params driver, an initalized selenium dirver
        @params latest_term, the latest term that you want to pull.
    """
    def navigate_to_latest_timetable(self,driver,latest_term):
        # constructing the latest term's id
        newid = 'SSR_DUMMY_RECV1$sels$'+str(latest_term)+'$$0'

        # using selenium to hunt for the element and click
        term_button = driver.find_element_by_id(newid)
        term_button.click()

        # more hunting for buttons.
        continue_button = driver.find_element_by_id('DERIVED_SSS_SCT_SSR_PB_GO')
        continue_button.click()
        
        # loading the new timetablepage...
        clock.sleep(5)
        
        # grab the source, format it, return to bs4
        new_formatted_result = driver.page_source
        soup = BeautifulSoup(new_formatted_result,"html.parser")

        return soup

    """
        Sort the type of classes.
        @params row, a row pulled from the thml
        @params class_type_dict, the dictionary to store the class type.
    """
    def __type_of_classes(self,row,class_type_dict):
        gettype = row.find("span",{"id":re.compile(r'(MTG_COMP\$)([0-9]{1})')})
        if not gettype.text:
            gettype = row.find("span",{"id":re.compile(r'(MTG_COMP\$)([0-9]{1})([0-9]{1})')})

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
    """
    def __get_row_id(self,row):
        getlocation = row.find("span",{'id':re.compile(r'(MTG_LOC\$)([0-9]{1})')})
        if not getlocation.text.strip():
            getlocation = row.find("span",{'id':re.compile(r'(MTG_LOC\$)([0-9]{1})([0-9]{1})')})

        rowid = (((getlocation.get('id')).split("$"))[1]).strip()
        return rowid

    def handle_single_digit_row(self,singledigittablerow,class_type_dict,list_of_results,subjectitlename):
        for row in singledigittablerow:
            # Instantiate a  new class object.
            class_object = IndividualClassStructure(subjectitlename)
            '''####################################################################################
                                    Here we're going to use regex.
                            Why do we repeat same regex twice with variance?
                            First we check for id with regex for single digit
                                    For example, MTG_DATES$0
                    If in that div, MTGDATES$# WHERE # is a random number does not match regex, 
                        It means that we're in a row where MTGDATES$ is MTGDATES$##
                                Thus we write another regex for that row.
                This was probably never meant to be pulled as an API that's why its so fucked up.
            ####################################################################################'''

            self.__type_of_classes(row,class_type_dict)

            # Sets the date of the class in the class object.
            class_object.set_date_of_class(row)
            # Sets the start time of the class
            class_object.set_time(True,row)
            # Sets the end time of the class
            class_object.set_time(False,row)
            # Sets the location of the class (where the class is being held.)
            class_object.set_location(row)
            # Time to determine class type (lecture, tutorial) from the array above.
            rowid = self.__get_row_id(row)          
            list_of_class_type_keys = list(class_type_dict.keys())
            list_of_class_type_keys = sorted(list_of_class_type_keys)
            no_of_keys = len(list_of_class_type_keys)

            class_object.determine_class_type(list_of_class_type_keys,class_type_dict,no_of_keys,rowid)

            list_of_results.append(class_object)
    """
        process the subject div.
        @ params subjectdiv, a div of subjects extracted from the html.
        @ params class_type_dict, an empty dictionary.
        @ params list_of_results, an empty list.
    """
    def process_subject_div(self,subjectdiv,class_type_dict,list_of_results):
        for div in subjectdiv:
            class_type_dict.clear()
            subjectitle = div.find("td",{'class':'PAGROUPDIVIDER'})
            subjectitlename = subjectitle.text
            singledigittablerow = div.findAll('tr',{'id':re.compile(r'(trCLASS_MTG_VW\$)([0-9]{1})(_row)([0-9]{1})')})
            self.handle_single_digit_row(singledigittablerow,class_type_dict,list_of_results,subjectitlename)
    """
        An override method for the super class.
    """        
    def execute(self):
        #"API" that populates timetable. It was never designed for this purpose, but we're going to use it
        #initialize PhantomJS, define settings
        driver = webdriver.PhantomJS(executable_path='./phantomjs',service_args=['--ignore-ssl-errors=true', '--ssl-protocol=TLSv1'])
        driver.set_window_size(1124, 850) 
        page_source = self.login(driver)
        if self.logout_url in page_source:
            driver.get(self.timetable_page) 
            formatted_result = driver.page_source
            soup = BeautifulSoup(formatted_result,"html.parser")
            termdiv = soup.findAll('span',{'id':re.compile(r'(TERM_CAR\$)([0-9]{1})')})

            # If there is more than 1 timetable avaliable, we default to the latest term's timetable.
            if len(termdiv) != 0:
                latest_term = len(termdiv)-1
                soup = self.navigate_to_latest_timetable(driver,latest_term)
            
            # list of all the subjects.
            subjectdiv = soup.findAll('div',{'id':re.compile(r'(win2divDERIVED_REGFRM1_DESCR20\$)([0-9]{1})')})
            class_type_dict = {}
            list_of_results = []

            self.process_subject_div(subjectdiv,class_type_dict,list_of_results)
            driver.close()
            return(list_of_results)
        else:
            driver.close()
            return []
"""
    Not really necessary, but I dont like calling a superclass blindly.
    Inherits from SIMConnect superclass.
"""
class LoginTest(SIMConnect):
    def __init__(self,username,password):
        super(LoginTest, self).__init__(username,password)


"""
    For testing purposes only.
"""
if __name__ == "__main__":
    # Loads an account from testing_accounts.json which is placed in .gitignore to
    # ensure that we don't accidentally commit our tester accounts to git.
    # Big thanks to Ray Keeve from UOB and See Yi Ze from UOL for volunteering to be guinea pigs.
    # If you would like to be a guinea pig for this project, drop me a mail at contact@jingk.ai
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
    with open ("testing_accounts.json") as json_file:
        data = json.load(json_file)
        try:
            data[user_to_load]
        except KeyError:
            print("Cannot find data in file")
            sys.exit()
        else:
            username = data[user_to_load]["username"]
            password = data[user_to_load]["password"]
            method = input("What type of test would you like to perform? (rip | login): ")
            if method == "rip":
                list_of_classes = (RipTimeTable(username,password).execute())
                for cl in list_of_classes:
                    print(cl.get_dict())
            elif method == "login":
                print(LoginTest(username,password).execute())
            else:
                print("Unknown method")
