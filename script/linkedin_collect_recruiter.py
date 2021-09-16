import os
import sys
import json


# 3d party
from linkedin_scraper import Person, actions

sys.path.append('../')
from bigbreaker.common.tools_identity import ToolsIdentity
from bigbreaker.common.system_webdriver import SystemWebdriver
from bigbreaker.google.tab_manager_google import TabManagerGoogle
from bigbreaker.linkedin.tab_manager_linkedin import TabManagerLinkedin
from bigbreaker.linkedin.linkedin_person import LinkedinPerson

with open('config.cfg', 'r') as file:
    config = json.load(file)

id_identity = 'identity_3'
identity = ToolsIdentity.identity_load(config, id_identity)
webdriver = ToolsIdentity.webdriver_load(config, id_identity)


email = identity['linkedin_username']
password = identity['linkedin_password']
# not needed? actions.login(webdriver, email, password) # if email and password isnt given, it'll prompt in terminal
id_linkedin_person = 'andre-iguodala-65b48ab5'
if not LinkedinPerson.linkedin_person_has_pkl(config, id_linkedin_person):
    print('scraping ' +  id_linkedin_person)
    person = Person("https://www.linkedin.com/in/" + id_linkedin_person, driver=webdriver)
    print(person)
    person.scrape_logged_in(close_on_complete=True)
    LinkedinPerson.linkedin_person_save_pkl(config, id_linkedin_person, person)
    
else:
    print('loading ' +  id_linkedin_person)
    person = LinkedinPerson.linkedin_person_load_pkl(config, id_linkedin_person)

print(person)