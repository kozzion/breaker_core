import os
import sys
import json
import time

from bigbreaker.common.system_webdriver import SystemWebdriver

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

class TabManagerGoogle:

    def __init__(self, webdriver, window_handle):
        super(TabManagerGoogle, self).__init__()
        self.webdriver = webdriver
        self.window_handle = window_handle
        self.current_url = ''
        self.username_logged_in = None

    def make_active(self):
        if not self.webdriver.current_window_handle == self.window_handle:
            self.webdriver.switch_to.window(str(self.window_handle))
            time.sleep(0.1)

    def action_get_url_first_hit(self, querry):
        print('action_load_list_jobitem')
        # dots linkedin new york
        self.make_active()
        SystemWebdriver.open_url(self.webdriver, 'https://www.google.com/ncr')
        SystemWebdriver.await_is_clickable(self.webdriver, "//input[@title='Search']")
        self.webdriver.find_element(By.XPATH, "//input[@title='Search']").send_keys(querry)
        self.webdriver.find_element(By.XPATH, "//input[@title='Search']").send_keys(Keys.RETURN)
        SystemWebdriver.await_is_present(self.webdriver, 'g')
        list_element_result = self.webdriver.find_elements_by_class_name('g')
        return self.parse_element_result(list_element_result[0])['url']

    def parse_element_result(self, element_result):
        result = {}
        result['url'] = element_result.find_element_by_tag_name("a").get_attribute("href")
        return result
