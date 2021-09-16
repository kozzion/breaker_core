
import os
import sys
import json
import time
from pynput.keyboard import Key, Controller


from bigbreaker.common.system_webdriver import SystemWebdriver
from bigbreaker.common.tab_manager_base import TabManagerBase
from bigbreaker.builtin.jobitem import Jobitem
from bigbreaker.onionmail.tab_manager_onionmail import TabManagerOnionmail

from selenium.webdriver.support.select import Select
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

class TabManagerLinkedin(TabManagerBase):

    def __init__(self, webdriver, window_handle):
        super(TabManagerLinkedin, self).__init__()
        self.webdriver = webdriver
        self.window_handle = window_handle
        # tab_manager_onionmail:TabManagerOnionmail
        # self.tab_manager_onionmail = tab_manager_onionmail



    def action_create_account(self, identity):
        print('action_create_account')
        self.make_active()

        if not identity["onionmail_is_created"]:
            raise Exception()

       
        
        email = identity["onionmail_address"]
        name_first_0 = identity["name_first_0"]
        name_last_0 = identity["name_last_0"]
        # username = identity["linkedin_username"]
        password = identity["linkedin_password"]

        # birthday_year = identity["birthday_year"]
        # birthday_month = identity["birthday_month"]
        # birthday_day = identity["birthday_day"]



        SystemWebdriver.open_url(self.webdriver, 'https://www.linkedin.com/signup/cold-join')

        SystemWebdriver.await_is_clickable(self.webdriver, "//input[@name='email-address']")
        self.webdriver.find_element(By.XPATH, "//input[@name='email-address']").send_keys(email)
        self.webdriver.find_element(By.XPATH, "//input[@name='password']").send_keys(password)
        self.webdriver.find_element_by_id('join-form-submit').click()

        SystemWebdriver.await_is_clickable(self.webdriver, "//input[@id='first-name']")
        self.webdriver.find_element_by_id('first-name').send_keys(name_first_0)
        self.webdriver.find_element_by_id('last-name').send_keys(name_last_0)
        self.webdriver.find_element_by_id('join-form-submit').click()
    
    def action_apply(self, config, jobitem, url_job):
        print('action_apply')
        self.make_active()
        SystemWebdriver.open_url(self.webdriver, url_job)

        is_present = SystemWebdriver.await_is_present(self.webdriver, 'post-apply-timeline__content', 1)
        if is_present:
            jobitem['status_apply'] = 'alreaddy_applied'
            Jobitem.jobitem_save(config, jobitem['id_jobitem'], jobitem)
            print('alreaddy_applied')
            return True

        is_present = SystemWebdriver.await_is_present(self.webdriver, 'artdeco-inline-feedback__message', 1)
        if is_present:
            jobitem['status_apply'] = 'application_closed'
            Jobitem.jobitem_save(config, jobitem['id_jobitem'], jobitem)
            print('application_closed')
            return False


        print('start_application')
        is_present = SystemWebdriver.await_is_present(self.webdriver, 'jobs-apply-button', 1)

        
        print('wait4')
        time.sleep(4)
        element_button_apply = self.webdriver.find_element_by_class_name('jobs-apply-button')
        if element_button_apply.get_attribute('data-control-name') == 'shareProfileThenExternalApplyControl':
            jobitem['status_apply'] = 'application_external'
            Jobitem.jobitem_save(config, jobitem['id_jobitem'], jobitem)
            print('application_external')
            self.action_complete_application_external()
        else:
            jobitem['status_apply'] = 'application_internal'
            Jobitem.jobitem_save(config, jobitem['id_jobitem'], jobitem)
            print('application_internal')
            self.action_complete_application_internal()
      
    def action_complete_application_external(self):
        print('action_complete_application_external')
        self.webdriver.find_element_by_class_name('jobs-apply-button').click()
        print('loaded')
        print('wait4')
        time.sleep(4)

        window_handle_new = self.webdriver.window_handles[-1]
        print(self.webdriver.title)
        self.webdriver.switch_to.window(str(window_handle_new))
        print(self.webdriver.title)
        print(self.webdriver.current_url)

        identity = {}
        identity['first_name_0'] = 'first_name'
        identity['last_name_0'] = 'last_name'
        identity['email'] = 'email'
        identity['location'] = 'location'
        identity['phone'] = 'phone'
        identity['url_linkedin'] = 'url_linkedin' 

        list_input = self.webdriver.find_elements_by_tag_name('input')
        print(len(list_input))
        for element_input in list_input:
            self.action_fill_input(element_input, identity)
            
        list_element_select = self.webdriver.find_elements_by_tag_name('select')
        print(len(list_element_select))
        for element_select in list_element_select:
            self.action_fill_input(element_select, identity)

        list_element_a = self.webdriver.find_elements_by_tag_name('a')
        for element_a in list_element_a:
            self.action_fill_input(element_a, identity)

    def action_fill_input(self, element_input, identity):
     
        # input section
        type = self.fill_input_type(element_input)
        if type == 'first_name':
            element_input.send_keys(identity['first_name_0'])
            return

        if type == 'last_name':
            element_input.send_keys(identity['last_name_0'])
            return

        if type == 'email':
            element_input.send_keys(identity['email'])
            return

        if type == 'location':
            element_input.send_keys(identity['location'])
            return

        if type == 'phone':
            element_input.send_keys(identity['phone'])
            return

        if type == 'input_url_linkedin':
            element_input.send_keys(identity['url_linkedin'])
            return

        if type == 'input_found_where':
            element_input.send_keys('The buildin website')
            return

        if type == 'input_preferred_name':
            element_input.send_keys(identity['first_name_0'] + ' ' + identity['last_name_0'])
            return

        # select section    
        if type == 'select_can_work':
            Select(element_input).select_by_visible_text('Yes')
            return

        if type == 'select_need_visa':
            Select(element_input).select_by_visible_text('Yes')
            return

        if type == 'select_gender':
            Select(element_input).select_by_visible_text('Male')
            return

        if type == 'select_hispanic':
            Select(element_input).select_by_visible_text('No')
            return

        if type == 'select_race':
            Select(element_input).select_by_visible_text('Decline To Self Identify')
            return

        if type == 'select_veteran':
            Select(element_input).select_by_visible_text('I am not a protected veteran')
            return

        if type == 'select_disability':
            Select(element_input).select_by_visible_text("No, I don't have a disability, or a history/record of having a disability")
            return
            
        if type == 'button_attach_resume':
            path_doc = 'C:\\project\\breaker\\resume.txt'
 
            element_input.click()
            time.sleep(2)
            keyboard = Controller()

            # Press and release space
            keyboard.press(Key.space)
            keyboard.release(Key.space)

            # Type a lower case A; this will work even if no key on the
            # physical keyboard is labelled 'A'
            keyboard.press('a')
            keyboard.release('a')

            # Type two upper case As
            keyboard.press('A')
            keyboard.release('A')

            with keyboard.pressed(Key.shift):
                keyboard.press('a')
                keyboard.release('a')

            # Type 'Hello World' using the shortcut type method
            keyboard.type('Hello World')
            
            # ActionChains(self.webdriver).send_keys(path_doc).perform()
            # ActionChains(self.webdriver).send_keys(Keys.ESCAPE).perform()

        # if type == 'button_attach_cover':
        #     element_input.click()
        #     ActionChains(self.webdriver).send_keys(Keys.ESCAPE).perform()

    def fill_input_type(self, element_input):
        element_id = element_input.get_attribute('id')

        if 'first_name' in element_id:
            return 'first_name'

        if 'last_name' in element_id:
            return 'last_name'

        if 'email' in element_id:
            return 'last_name'

        if 'job_application_location' in element_id:
            return 'location'

        if 'phone' in element_id:
            return 'phone'

        if 'job_application_answers_attributes_2_text_value' in element_id:
            return 'input_url_linkedin'

        if 'job_application_answers_attributes_4_text_value' in element_id:
            return 'input_found_where'   

        if 'job_application_answers_attributes_5_text_value' in element_id:
            return 'input_preferred_name'   

        # select

        if 'job_application_answers_attributes_0_boolean_value' in element_id:
            return 'select_can_work'

        if 'job_application_answers_attributes_1_boolean_value' in element_id:
            return 'select_need_visa'




        if 'job_application_gender' in element_id:
            return 'select_gender'

        if 'job_application_hispanic_ethnicity' in element_id:
            return 'select_hispanic'

        if 'job_application_race' in element_id:
            return 'select_race'

        if 'job_application_veteran_status' in element_id:
            return 'select_veteran'

        if 'job_application_disability_status' in element_id:
            return 'select_disability'

        # attach
        if self.attribute_contains(element_input, 'data-source', 'attach'):
            if self.attribute_contains(element_input, 'aria-labelledby', 'resume'):
                return 'button_attach_resume'      
            if self.attribute_contains(element_input, 'aria-labelledby', 'cover_letter'):
                return 'button_attach_cover'

    def attribute_contains(self, element, atribute, contain):
        value = element.get_attribute(atribute)
        if value:
            return contain in value
        else:
            return False

    def action_complete_application_internal(self):
        print('action_complete_application_internal')
        self.webdriver.find_element_by_class_name('jobs-apply-button').click()
        print('clicked apply')

        SystemWebdriver.await_is_clickable(self.webdriver, "//button[@aria-label='Continue to next step']")
        self.webdriver.find_element(By.XPATH, "//button[@aria-label='Continue to next step']").click()
        
        
        SystemWebdriver.await_is_clickable(self.webdriver, "//button[@aria-label='Continue to next step']")
        print('add cover letter')
        # todo do, generate cover letter
        self.webdriver.find_element(By.XPATH, "//button[@aria-label='Continue to next step']").click()

        SystemWebdriver.await_is_clickable(self.webdriver, "//button[@aria-label='Continue to next step']")
        print('fill drop downs')
        list_element_select = self.webdriver.find_elements_by_tag_name('select')
        for element_select in list_element_select:
            element_select_typed = Select(element_select)
            list_option = [option.text for option in element_select_typed.options]
            if 'Male' in list_option:
                element_select_typed.select_by_visible_text('Male')
            if 'American Indian or Alaskan Native' in list_option:
                element_select_typed.select_by_visible_text('Decline To Self Identify')

            prefered_option = 'I am not a protected veteran'
            if prefered_option in list_option:
                element_select_typed.select_by_visible_text(prefered_option)

            prefered_option = "No, I don't have a disability, or a history/record of having a disability"
            if prefered_option in list_option:
                element_select_typed.select_by_visible_text(prefered_option)
        self.webdriver.find_element(By.XPATH, "//button[@aria-label='Continue to next step']").click()  

        SystemWebdriver.await_is_clickable(self.webdriver, "//button[@aria-label='Review your application']")   
        self.webdriver.find_element(By.XPATH, "//button[@aria-label='Review your application']").click()

                   
        SystemWebdriver.await_is_clickable(self.webdriver, "//button[@aria-label='Submit application']")
        print('unfollow')
        self.webdriver.find_element_by_id("follow-company-checkbox").click()
        exit()
        self.webdriver.find_element(By.XPATH, "//button[@aria-label='Submit application']")