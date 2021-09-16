import random
import string
import json
import sys
import os
import pathlib



sys.path.append('../')
from bigbreaker.common.tools_identity import ToolsIdentity
from bigbreaker.common.system_webdriver import SystemWebdriver
from bigbreaker.google.tab_manager_google import TabManagerGoogle
from bigbreaker.builtin.jobitem import Jobitem


with open('config.cfg', 'r') as file:
    config = json.load(file)

id_identity = 'identity_0'
identity = ToolsIdentity.identity_load(config, id_identity)
webdriver = ToolsIdentity.webdriver_load(config, id_identity)
handle_builtin = webdriver.window_handles[0]

tab_manager_google = TabManagerGoogle(webdriver, handle_builtin) 

list_jobitem = Jobitem.jobitem_load_list(config)
print(len(list_jobitem))
for jobitem in list_jobitem:
    querry ='site:www.linkedin.com/jobs'
    title = jobitem['title']
    if ',' in title:
        title = title.split(',')[0].strip()
    querry += ' ' + title
    querry += ' ' + jobitem['name_company']
    print(querry)
    url_linkedin = tab_manager_google.action_get_url_first_hit(querry)
    print(url_linkedin)  
    jobitem['url_linkedin'] = url_linkedin
    Jobitem.jobitem_save(config, jobitem['id_jobitem'], jobitem)
    
  
