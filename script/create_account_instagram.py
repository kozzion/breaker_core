import random
import string
import json
import sys
import os
import pathlib



sys.path.append('../')
from bigbreaker.common.tools_identity import ToolsIdentity
from bigbreaker.common.system_webdriver import SystemWebdriver
from bigbreaker.onionmail.tab_manager_onionmail import TabManagerOnionmail
from bigbreaker.instagram.tab_manager_instagram import TabManagerInstagram

with open('config.cfg', 'r') as file:
    config = json.load(file)

id_identity = 'identity_1'
identity = ToolsIdentity.identity_load(config, id_identity)
webdriver = ToolsIdentity.webdriver_load(config, id_identity)
handle_onionmail = webdriver.window_handles[0]
handle_instagram = SystemWebdriver.open_tab(webdriver)

tab_manager_onionmail = TabManagerOnionmail(webdriver, handle_onionmail) 
tab_manager_instagram = TabManagerInstagram(webdriver, handle_instagram, tab_manager_onionmail)

tab_manager_instagram.action_create_account(identity)
identity['instagram_is_created'] = True
ToolsIdentity.identity_save(config, id_identity, identity)
