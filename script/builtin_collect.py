import random
import string
import json
import sys
import os
import pathlib



sys.path.append('../')
from bigbreaker.common.tools_identity import ToolsIdentity
from bigbreaker.common.system_webdriver import SystemWebdriver
from bigbreaker.builtin.tab_manager_builtin import TabManagerBuiltin
from bigbreaker.builtin.jobitem import Jobitem

with open('config.cfg', 'r') as file:
    config = json.load(file)

id_identity = 'identity_0'
identity = ToolsIdentity.identity_load(config, id_identity)
webdriver = ToolsIdentity.webdriver_load(config, id_identity)
handle_builtin = webdriver.window_handles[0]

tab_manager_builtin = TabManagerBuiltin(webdriver, handle_builtin) 


list_jobitem = tab_manager_builtin.action_load_list_jobitem()

print(len(list_jobitem))
for jobitem in list_jobitem:
    Jobitem.jobitem_save(config, jobitem['id_jobitem'], jobitem)
    print(jobitem['title'])
    print(jobitem['name_company'])
    print()
