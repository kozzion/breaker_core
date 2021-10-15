
import os
import sys
import json
import time
from pynput.keyboard import Key, Controller


from breaker_core.common.system_webdriver import SystemWebdriver
from breaker_core.common.tab_manager_base import TabManagerBase
from breaker_core.builtin.jobitem import Jobitem
from breaker_core.onionmail.tab_manager_onionmail import TabManagerOnionmail
from breaker_core.common.tools_input import ToolsInput

from selenium.webdriver.support.select import Select
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

class TabManagerLinkedin(TabManagerBase):

    def __init__(self, config, webdriver, window_handle):
        super(TabManagerLinkedin, self).__init__()
        self.config = config
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
        self.webdriver.find_element(By.ID, 'join-form-submit').click()

        SystemWebdriver.await_is_clickable(self.webdriver, "//input[@id='first-name']")
        self.webdriver.find_element(By.ID, 'first-name').send_keys(name_first_0)
        self.webdriver.find_element(By.ID, 'last-name').send_keys(name_last_0)
        self.webdriver.find_element(By.ID, 'join-form-submit').click()
    
    def action_apply(self, config, jobitem, tab_manager_google, identity):
        print('action_apply')
        id_jobitem = jobitem['id_jobitem']

        if not 'url_job' in jobitem:
            querry ='site:www.linkedin.com/jobs'
            title = jobitem['title']
            if ',' in title:
                title = title.split(',')[0].strip()
            querry += ' ' + title
            querry += ' ' + jobitem['name_company']
            print(querry)
            url_job = tab_manager_google.action_get_url_first_hit(querry)

        
            # https://www.linkedin.com/jobs/view/
            if not 'https://www.linkedin.com/jobs/view/' in url_job:
                Jobitem.jobitem_status_update(config, id_jobitem, 'application_broken_link')
                print('application_broken_link')
                return

            jobitem['url_job'] = url_job
            Jobitem.jobitem_save(config, id_jobitem, jobitem)
        else:
            url_job = jobitem['url_job']
   
        self.make_active()
        SystemWebdriver.open_url(self.webdriver, url_job)

        is_present, element = SystemWebdriver.await_is_present(self.webdriver, 'post-apply-timeline__content', 1)
        if is_present:
            Jobitem.jobitem_status_update(config, id_jobitem, 'application_complete')
            print('application_complete')
            return

        is_present, element = SystemWebdriver.await_is_present(self.webdriver, 'artdeco-inline-feedback__message', 1)
        if is_present:
            Jobitem.jobitem_status_update(config, id_jobitem, 'application_closed')
            print('application_closed')
            return
        
        print('start_application')
        is_present, element_button_apply = SystemWebdriver.await_is_present_any(self.webdriver, ['apply-button', 'jobs-apply-button'], 1)
        if not is_present:
            print('application button not found')
            exit()

        if jobitem['status_apply'] == 'application_started':
            print('application_started')
        else:
            jobitem['status_apply']
            option = ToolsInput.promt_option('Apply to this job?', ['Apply never', 'Postpone', 'Apply now', 'Have applied'])
            if option == 'Apply never':
                print('Apply never')
                Jobitem.jobitem_status_update(config, id_jobitem, 'application_discarded')
                return
            elif option == 'Postpone':
                print('Postpone')
                Jobitem.jobitem_status_update(config, id_jobitem, 'application_postponed')
                return
            elif option == 'Apply now':
                print('Apply now')
                Jobitem.jobitem_status_update(config, id_jobitem, 'application_started')
            elif option == 'Have applied':
                print('Have applied')
                Jobitem.jobitem_status_update(config, id_jobitem, 'application_complete')
                return
            else:
                raise Exception('Unknown option: ' + option)
        
        
        print('wait2')
        time.sleep(2)
        print(element_button_apply.get_attribute("innerHTML"))
        if element_button_apply.get_attribute('data-is-offsite-apply') == "true":
            # jobitem['status_apply'] = 'application_external'
            # Jobitem.jobitem_save(config, jobitem['id_jobitem'], jobitem)
            print('application_external')

            url_form_apply = element_button_apply.get_attribute("href")
            tab_handle_new = SystemWebdriver.open_tab(self.webdriver)
            self.webdriver.switch_to.window(str(tab_handle_new))
            SystemWebdriver.open_url(self.webdriver, url_form_apply)            
            self.action_complete_application_external(jobitem, identity)


        elif element_button_apply.get_attribute('data-control-name') == 'shareProfileThenExternalApplyControl':
            # jobitem['status_apply'] = 'application_external'
            # Jobitem.jobitem_save(config, jobitem['id_jobitem'], jobitem)
            print('application_external')
            element_button_apply.click()
            self.action_complete_application_external(jobitem, identity)
   
            

        elif element_button_apply.get_attribute('data-control-name') == 'public_jobs_apply-link-offsite':
            # jobitem['status_apply'] = 'application_external'
            # Jobitem.jobitem_save(config, jobitem['id_jobitem'], jobitem)
            print('application_external')
            element_button_apply.click()
            tab_handle_new = self.webdriver.window_handles[-1]
            print(self.webdriver.title)
            self.webdriver.switch_to.window(str(tab_handle_new))
            print(self.webdriver.title)
            print(self.webdriver.current_url)
            self.action_complete_application_external(jobitem, identity)

        else:
            # jobitem['status_apply'] = 'application_internal'
            # Jobitem.jobitem_save(config, jobitem['id_jobitem'], jobitem)
            print('application_internal')
            self.action_complete_application_internal(jobitem, identity)
      
    def action_complete_application_external(self, jobitem, identity):
        print('action_complete_application_external')
        print('loaded')
        print('wait2')
        sys.stdout.flush()
        time.sleep(2)

        window_handle_new = self.webdriver.window_handles[-1]
        print(self.webdriver.title)
        self.webdriver.switch_to.window(str(window_handle_new))
        print(self.webdriver.title)
        print(self.webdriver.current_url)
        SystemWebdriver.await_is_loaded(self.webdriver)
        print('wait220')
        sys.stdout.flush()
        time.sleep(2)

        
        list_iframe = self.webdriver.find_elements(By.ID, 'grnhse_iframe')
        source_element = self.webdriver 
        if 0 < len(list_iframe):
            print('found_linkedin_iframe')
            # source_element = list_iframe[0]
            self.webdriver.switch_to.frame(list_iframe[0])

        list_input = source_element.find_elements(By.TAG_NAME, 'input')
        print(len(list_input))
        for element_input in list_input:
            self.action_fill_input(element_input, jobitem, identity)
            
        list_element_select = source_element.find_elements(By.TAG_NAME, 'select')
        print(len(list_element_select))
        for element_select in list_element_select:
            self.action_fill_input(element_select, jobitem, identity)

        list_element_a = source_element.find_elements(By.TAG_NAME, 'a')
        print(len(list_element_a))
        for element_a in list_element_a:
            self.action_fill_input(element_a, jobitem, identity)
            
        # element_question = source_element.find_element(By.ID, 'job_application_answers_attributes_1_text_value')
        # print(self.find_descibing_list_text(element_question))

    def action_fill_input(self, element_input, jobitem, identity):
     
     
        # input section
        type = self.fill_input_type(element_input)
        if type == 'first_name':
            element_input.send_keys(identity['name_first_0'])
            return

        if type == 'last_name':
            element_input.send_keys(identity['name_last_0'])
            return

        if type == 'email':
            element_input.send_keys(identity['email_primary'])
            return

        if type == 'location':
            element_input.send_keys(identity['location_current_city'])
            return

        if type == 'phone':
            element_input.send_keys(identity['phone_primary'])
            return

        if type == 'input_url_linkedin':
            element_input.send_keys(identity['url_linkedin'])
            return

        if type == 'input_found_where':
            element_input.send_keys('The builtin website')
            return

        if type == 'input_preferred_name':
            element_input.send_keys(identity['name_first_0'] + ' ' + identity['name_last_0'])
            return

        if type == 'input_can_work':
            element_input.send_keys('No')
            return

        if type == 'input_salary_expectations':
            element_input.send_keys('150000USD per year')
            return


        if type == 'input_personal_website':
            element_input.send_keys(identity['url_github'])
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
            path_file_resume = 'C:\\project\\data\\data_breaker\\CV_20210809_us.pdf'
            self.upload_file(element_input, path_file_resume)

        if type == 'button_attach_cover':
            Jobitem.generate_cover_letter(self.config, jobitem, identity)
            path_file_cover = Jobitem.coverletterpdf_load_path(self.config, jobitem['id_jobitem'])
            print(path_file_cover)
            self.upload_file(element_input, path_file_cover)

    def fill_input_type(self, element_input):
        element_id = element_input.get_attribute('id')
        if element_input.get_attribute('type') == 'hidden': 
            return 'unknown'
            
        if 'first_name' in element_id:
            return 'first_name'

        if 'last_name' in element_id:
            return 'last_name'

        if 'email' in element_id:
            return 'email'

        if 'job_application_location' in element_id:
            return 'location'

        if 'phone' in element_id:
            return 'phone'

        
        # if 'job_application_answers_attributes_2_text_value' in element_id:
        #     return 'input_url_linkedin'

        # if 'job_application_answers_attributes_4_text_value' in element_id:
        #     return 'input_found_where'   

        # if 'job_application_answers_attributes_5_text_value' in element_id:
        #     return 'input_preferred_name'   

        # # select

        # if 'job_application_answers_attributes_0_boolean_value' in element_id:
        #     return 'select_can_work'

        # if 'job_application_answers_attributes_1_boolean_value' in element_id:
        #     return 'select_need_visa'




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

        if len(element_id.strip()) == 0:
            return 'unknown'

        if element_id == 'submit_app':
            return 'unknown'

   
        list_description = self.find_descibing_list_text(element_input)
        if ToolsInput.match(list_description, 'LinkedIn Profile'): 
            return 'input_url_linkedin'
        
        if ToolsInput.match(list_description, 'hear about this job'): 
            return 'input_found_where'

        if ToolsInput.match(list_description, 'employer without restrictions?'): 
            return 'input_can_work'

        if ToolsInput.match(list_description, 'What are your current salary expectations'): 
            return 'input_salary_expectations'
            
        if ToolsInput.match(list_description, 'name or nickname?'): 
            return 'input_preferred_name'

        if ToolsInput.match(list_description, 'Website'): 
            return 'input_personal_website'
            
            

        print(element_id)
        print(list_description)     
        return 'unknown'

    def attribute_contains(self, element, atribute, contain):
        value = element.get_attribute(atribute)
        if value:
            return contain in value
        else:
            return False

    def action_complete_application_internal(self, jobitem, identity):
        print('action_complete_application_internal')
        self.webdriver.find_element(By.CLASS_NAME,'jobs-apply-button').click()
        print('clicked apply')

        SystemWebdriver.await_is_clickable(self.webdriver, "//button[@aria-label='Continue to next step']")
        self.webdriver.find_element(By.XPATH, "//button[@aria-label='Continue to next step']").click()
        
        
        SystemWebdriver.await_is_clickable(self.webdriver, "//button[@aria-label='Continue to next step']")
        print('add cover letter')
        sys.stdout.flush()
        Jobitem.generate_cover_letter(self.config, jobitem, identity)
        path_file_cover = Jobitem.coverletterpdf_load_path(self.config, jobitem['id_jobitem'])
        print(path_file_cover)
        element_upload_parent = self.find_parent(self.find_elements_by_inner_html_equals(self.webdriver, By.TAG_NAME, 'span', 'Upload cover letter')[0])
        self.upload_file(element_upload_parent, path_file_cover)
        time.sleep(1)
        self.webdriver.find_element(By.XPATH, "//button[@aria-label='Continue to next step']").click()

        SystemWebdriver.await_is_clickable(self.webdriver, "//button[@aria-label='Continue to next step']")
        print('fill drop downs')
        sys.stdout.flush()
        list_element_select = self.webdriver.find_elements(By.TAG_NAME, 'select')
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
        

        SystemWebdriver.await_is_clickable(self.webdriver, "//button[@aria-label='Continue to next step']")
        print('show website')
        sys.stdout.flush()
        self.webdriver.find_element(By.XPATH, "//button[@aria-label='Continue to next step']").click()

        SystemWebdriver.await_is_clickable(self.webdriver, "//button[@aria-label='Review your application']")   
        print('fill dropdowns visa')
        sys.stdout.flush()
        list_element_select = self.webdriver.find_elements(By.TAG_NAME, 'select')
        print(len(list_element_select))
        for element_select in list_element_select:
            list_text = self.find_descibing_list_text(element_select)
            if ToolsInput.match(list_text, 'Are you legally authorized to work in the United States?'):
                Select(element_select).select_by_visible_text('No')

            if ToolsInput.match(list_text, 'Will you now or in the future require sponsorship for employment'):
                Select(element_select).select_by_visible_text('Yes') 

        self.webdriver.find_element(By.XPATH, "//button[@aria-label='Review your application']").click()

                   
        SystemWebdriver.await_is_clickable(self.webdriver, "//button[@aria-label='Submit application']")
        promt = ToolsInput.promt_option('complete application?', ['Yes', 'No'])
        if promt == 'Yes':
            print('application_complete')
            Jobitem.jobitem_status_update(self.config, jobitem['id_jobitem'], 'application_complete')
            self.webdriver.find_element(By.XPATH, "//button[@aria-label='Submit application']").click()
        else:
            print('application_postponed')
            Jobitem.jobitem_status_update(self.config, jobitem['id_jobitem'], 'application_postponed')
