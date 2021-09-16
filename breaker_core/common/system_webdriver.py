import sys
import os
import json
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

class SystemWebdriver(object):

    def __init__(self, path_file_executable):
        super(SystemWebdriver, self).__init__()
        self.path_file_executable = path_file_executable
        self.state = {}

    @staticmethod
    def is_loaded(webdriver):
        return webdriver.execute_script("return document.readyState") == "complete"
    
    @staticmethod
    def await_is_loaded(webdriver):
        while(not SystemWebdriver.is_loaded(webdriver)):
            sys.stdout.flush()
            time.sleep(0.1)

    @staticmethod
    def await_is_clickable(webdriver, xpath, timeout_s=20):
        WebDriverWait(webdriver, timeout_s).until(EC.element_to_be_clickable((By.XPATH, xpath)))

        
    @staticmethod
    def await_is_present(webdriver, name_class, timeout_s=20, verbose=False):
        list_element = webdriver.find_elements_by_class_name(name_class)
        for i in range(int(timeout_s/0.1)):
            list_element = webdriver.find_elements_by_class_name(name_class)
            if 0 < len(list_element):
                return True

            time.sleep(0.1)
            if verbose:
                print('sleep')
                sys.stdout.flush()
        return False

    @staticmethod
    def open_url(webdriver, url):    
        #if not self.current_url == url:
        webdriver.get(url)
        SystemWebdriver.await_is_loaded(webdriver)

    @staticmethod
    def find_first_tag_with_innerhtml(webdriver, tag, inner_html):
        list_element_button = webdriver.find_elements_by_tag_name(tag)
        for element_button in list_element_button:
            if element_button.get_attribute('innerHTML') == inner_html:
                return element_button

    @staticmethod
    def get_handle(webdriver, index_handle):
        while(len(webdriver.window_handles) < index_handle + 1):
            SystemWebdriver.open_tab(webdriver)
        return webdriver.window_handles[index_handle]

    @staticmethod
    def open_tab(webdriver):
        webdriver.execute_script("window.open('');")
        return webdriver.window_handles[-1]

    def save(self):
        pass

    def load(self):
        pass

    def add_webdriver(self, name, path_dir_folder):
        pass
   

    def session_reconnect(self, path_file_session):
        try:
            with open(path_file_session, 'r') as file:
                session = json.load(file)
            chrome_options = Options()
            chrome_options.add_argument("--headless")
            driver = webdriver.Remote(command_executor=session['url'], desired_capabilities={}, options=chrome_options) # this opens a new windw
            driver.session_id = session['session_id']
            return driver
        except Exception:
            return None


    def session_create_new(self, path_file_session, path_dir_userdata):
        chrome_options = Options()
        chrome_options.add_argument("user-data-dir=" + path_dir_userdata) 
        driver = webdriver.Chrome(executable_path=self.path_file_executable, chrome_options=chrome_options)
        session = {}
        session['url'] = driver.command_executor._url
        session['session_id'] = driver.session_id
        with open(path_file_session, 'w') as file:
            json.dump(session, file)
        return driver

    def is_alive(self, driver):
        if driver == None:
            return False
        try:
            print(driver.title)
            return True
        except WebDriverException:
            return False


    def get_webdriver(self, path_file_session, path_dir_userdata):
        driver = self.session_reconnect(path_file_session)
        if not self.is_alive(driver):
            driver = self.session_create_new(path_file_session, path_dir_userdata)
        return driver

