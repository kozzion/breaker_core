import os
import sys
import json
import time

from bigbreaker.common.system_webdriver import SystemWebdriver

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

class TabManagerOnionmail:

    def __init__(self, webdriver, window_handle):
        super(TabManagerOnionmail, self).__init__()
        self.webdriver = webdriver
        self.window_handle = window_handle
        self.current_url = ''
        self.username_logged_in = None

    def make_active(self):
        if not self.webdriver.current_window_handle == self.window_handle:
            self.webdriver.switch_to.window(str(self.window_handle))
            time.sleep(0.1)

    def action_create_account(self, identity):
        self.make_active()
        SystemWebdriver.open_url(self.webdriver, 'https://www.onionmail.org/account/create/')
        name = identity["name_first_0"] + " " + identity["name_last_0"]
        username = identity["onionmail_username"]
        password = identity["onionmail_password"]
        #WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//input[@class='inputlong' and @id='identificacionUsuario']"))).send_keys("your_name")
        self.webdriver.find_element_by_id("name").send_keys(name)
        self.webdriver.find_element_by_id("username").send_keys(username)
        self.webdriver.find_element_by_id("password").send_keys(password)
        self.webdriver.find_element_by_id("password2").send_keys(password)
        element = self.webdriver.find_element_by_name("remember")
        if not element.is_selected():
            element.click()
        self.webdriver.find_element_by_class_name("btn-success").click()

    def action_load_list_html_email_recent(self, identity):
        print('action_load_list_html_email_recent')
        self.make_active()
        #self.action_make_logged_in(identity)
        username = identity["onionmail_username"]
        if not self.username_logged_in == username:
            self.action_logout()
            self.action_login(identity)
            
        list_url_message = self.load_list_url_message()
        for url_message in list_url_message:
            html_email = self.action_load_html_email(url_message)

    def action_logout(self):
        self.make_active()
        pass

    def action_login(self, identity):
        print('action_login')
        self.make_active()
        username = identity["onionmail_username"]
        password = identity["onionmail_password"]
        SystemWebdriver.open_url(self.webdriver, 'https://www.onionmail.org/account/login/')
        self.webdriver.find_element_by_id("username").send_keys(username)
        self.webdriver.find_element_by_id("password").send_keys(password)
        element = self.webdriver.find_element_by_name("remember")
        if not element.is_selected():
            element.click()            
        self.webdriver.find_element_by_class_name("btn-success").click()

    def action_load_html_email(self, url_message): 
        self.make_active()       
        SystemWebdriver.open_url(self.webdriver, url_message)
        #TODO
        # element = self.webdriver.find_element_by_name("remember")
        # if not element.is_selected():
        #     element.click()            
        # self.webdriver.find_element_by_class_name("btn-success").click()

    def action_load_instagram_code_recent(self, identity):
        self.make_active()
        self.action_login(identity) # TODO
        list_email_reference = self.load_list_email_reference_recent()
        for email_reference in list_email_reference:
            if email_reference['email_sender'] == 'no-reply@mail.instagram.com':
                if 'is your Instagram code' in email_reference['subject']:
                    code = email_reference['subject'].split(' ')[0]
                    return code
        
        return None
        


    def load_list_email_reference_recent(self):
        self.make_active()
        list_element = self.webdriver.find_elements_by_class_name("messagerow")
        list_email_reference = []
        for element in list_element:
            email_reference = {}
            email_reference['href'] = element.find_element_by_class_name("messagerow-link").get_attribute("href")
            email_reference['email_sender'] = element.find_element_by_class_name("mp_address_email").get_attribute("data-original-title")
            email_reference['subject'] = element.find_element_by_class_name("messagerow-subject-content").get_attribute("innerHTML").split('<span')[0][1:]
            email_reference['datetime'] = element.find_element_by_class_name("datestring-fixed").get_attribute("title")
            list_email_reference.append(email_reference)
        return list_email_reference
            
    
        
        
    def load_list_url_message(self):
        list_element = self.webdriver.find_elements_by_class_name("messagerow")
        list_url_message = []
        for element in list_element:
            element_href = element.find_element_by_class_name("messagerow-link")
            list_url_message.append(element_href.get_attribute("href")) 
        return list_url_message
            
    
        