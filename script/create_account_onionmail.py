import random
import string
import json
import sys
import os
import pathlib



sys.path.append('../')
from bigbreaker.common.tools_identity import ToolsIdentity
from bigbreaker.onionmail.tab_manager_onionmail import TabManagerOnionmail

with open('config.cfg', 'r') as file:
    config = json.load(file)

id_identity = 'identity_3'
if not ToolsIdentity.identity_has(config, id_identity):
    identity = ToolsIdentity.identity_create(config, id_identity)
else:
    identity = ToolsIdentity.identity_load(config, id_identity)

webdriver = ToolsIdentity.webdriver_load(config, id_identity)

page_manager = TabManagerOnionmail(webdriver, webdriver.window_handles[0])
page_manager.action_create_account(identity)
identity['onionmail_is_created'] = True
ToolsIdentity.identity_save(config, id_identity, identity)

page_manager.action_login(identity)