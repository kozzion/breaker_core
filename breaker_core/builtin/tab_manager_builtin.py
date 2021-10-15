import os
import sys
import json
import time

from breaker_core.common.system_webdriver import SystemWebdriver

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

    def action_load_list_jobitem(self):
        print('action_load_list_jobitem')
        self.make_active()
        # url = 'https://www.builtinnyc.com/jobs/office-remote/new-york-city/data-analytics/senior?ni=4'
        url = 'https://www.builtinnyc.com/jobs/office-remote/new-york-city/data-analytics/data-science/machine-learning/senior?ni=4'
        SystemWebdriver.open_url(self.webdriver, url)
        list_jobitem = []
        SystemWebdriver.await_is_present(self.webdriver, 'job-row')
        list_element_jobitem = self.webdriver.find_elements(By.CLASS_NAME, 'job-item')
        for element_jobitem in list_element_jobitem:
            list_jobitem.append(self.parse_element_jobitem(element_jobitem))
        
        count_page = 1
        list_element_pagelink = self.webdriver.find_elements(By.CLASS_NAME, 'page-link')
        for pagelink in list_element_pagelink:
            try:
                count_page = max(count_page, int(pagelink.get_attribute("innerHTML")))
            except:
                pass
 
        for index_page in range(2, count_page + 1):
            print(index_page)
            url = 'https://www.builtinnyc.com/jobs/office-remote/new-york-city/data-analytics/data-science/machine-learning/senior?ni=4&page=' + str(index_page)
            SystemWebdriver.open_url(self.webdriver, url)
            SystemWebdriver.await_is_present(self.webdriver, 'job-row')
            list_element_jobitem = self.webdriver.find_elements(By.CLASS_NAME,'job-item')
            for element_jobitem in list_element_jobitem:
                list_jobitem.append(self.parse_element_jobitem(element_jobitem))

        return list_jobitem



    def parse_element_jobitem(self, element_jobitem):
        jobitem = {}
        jobitem['title'] = element_jobitem.find_element(By.CLASS_NAME, "job-title").get_attribute("innerHTML")
        jobitem['url_jobitem'] = element_jobitem.find_element(By.CLASS_NAME, "external-link").get_attribute("href")
        jobitem['description'] = element_jobitem.find_element(By.CLASS_NAME, "job-description").get_attribute("innerHTML")
        jobitem['id_jobitem'] = jobitem['url_jobitem'].split('/')[-1]
        jobitem['name_company'] = element_jobitem.find_element(By.CLASS_NAME, "basic-info").find_elements(By.TAG_NAME, "span")[0].get_attribute("innerHTML")
        return jobitem