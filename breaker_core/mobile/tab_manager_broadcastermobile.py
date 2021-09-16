import os
import sys
import json
import time

from bigbreaker.common.system_webdriver import SystemWebdriver

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

class TabManagerBuiltin:

    def __init__(self, webdriver, window_handle):
        super(TabManagerBuiltin, self).__init__()
        self.webdriver = webdriver
        self.window_handle = window_handle
        self.current_url = ''
        self.username_logged_in = None

    def make_active(self):
        if not self.webdriver.current_window_handle == self.window_handle:
            self.webdriver.switch_to.window(str(self.window_handle))
            time.sleep(0.1)

    def action_create_account(self):
        print('action_load_list_jobitem')
        self.make_active()
        SystemWebdriver.open_url(self.webdriver, 'https://www.broadcastermobile.com/registra_tu_cuenta_gratis.html')
        SystemWebdriver.await_is_present(self.webdriver, 'job-row')
        list_element_jobitem = self.webdriver.find_elements_by_class_name('job-item')
        list_jobitem = []
        for element_jobitem in list_element_jobitem:
            list_jobitem.append(self.parse_element_jobitem(element_jobitem))
        return list_jobitem


    
        # TODO
        # https://dashboard.nexmo.com/sign-up
        # TODO 
        # https://www.broadcastermobile.com/registra_tu_cuenta_gratis.html


        bVjo8V99r3Km

    
