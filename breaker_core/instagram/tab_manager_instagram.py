import os
import sys
import json
import time

from bigbreaker.common.system_webdriver import SystemWebdriver
from bigbreaker.onionmail.tab_manager_onionmail import TabManagerOnionmail

from selenium.webdriver.support.select import Select
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

class TabManagerInstagram:

    def __init__(self, webdriver, window_handle, tab_manager_onionmail:TabManagerOnionmail):
        super(TabManagerInstagram, self).__init__()
        self.webdriver = webdriver
        self.window_handle = window_handle
        self.tab_manager_onionmail = tab_manager_onionmail

    def make_active(self):
        if not self.webdriver.current_window_handle == self.window_handle:
            self.webdriver.switch_to.window(str(self.window_handle))
            time.sleep(0.1)

    def action_create_account(self, identity):
        self.make_active()

        if not identity["onionmail_is_created"]:
            raise Exception()

       
        
        email = identity["onionmail_address"]
        name_full = identity["name_full"]
        username = identity["instagram_username"]
        password = identity["instagram_password"]

        birthday_year = identity["birthday_year"]
        birthday_month = identity["birthday_month"]
        birthday_day = identity["birthday_day"]



        SystemWebdriver.open_url(self.webdriver, 'https://www.instagram.com/accounts/emailsignup/?hl=en')
        SystemWebdriver.await_is_clickable(self.webdriver, "//input[@aria-label='Mobile Number or Email']")

        self.webdriver.find_element(By.XPATH, "//input[@aria-label='Mobile Number or Email']").send_keys(email)
        self.webdriver.find_element(By.XPATH, "//input[@aria-label='Full Name']").send_keys(name_full)
        self.webdriver.find_element(By.XPATH, "//input[@aria-label='Username']").send_keys(username)
        self.webdriver.find_element(By.XPATH, "//input[@aria-label='Password']").send_keys(password)

        self.webdriver.find_element(By.XPATH, "//button[@type='submit']").click()

        SystemWebdriver.await_is_clickable(self.webdriver, "//select[@title='Month:']")
        Select(self.webdriver.find_element(By.XPATH, "//select[@title='Month:']")).select_by_index(birthday_month - 1)
        Select(self.webdriver.find_element(By.XPATH, "//select[@title='Day:']")).select_by_index(birthday_day)
        Select(self.webdriver.find_element(By.XPATH, "//select[@title='Year:']")).select_by_visible_text(str(birthday_year))

        SystemWebdriver.find_first_tag_with_innerhtml(self.webdriver, 'button', 'Next').click()
        SystemWebdriver.await_is_clickable(self.webdriver, "//input[@aria-label='Confirmation Code']")
        time.sleep(10)

        code = self.tab_manager_onionmail.action_load_instagram_code_recent(identity)
        self.webdriver.find_element(By.XPATH, "//input[@aria-label='Confirmation Code']").send_keys(code)
        SystemWebdriver.find_first_tag_with_innerhtml(self.webdriver, 'button', 'Next').click()
        # actions = ActionChains(self.driver)      
        # actions.key_down(Keys.CONTROL).key_down(Keys.TAB).key_up(Keys.TAB).key_up(Keys.CONTROL).perform()

        
