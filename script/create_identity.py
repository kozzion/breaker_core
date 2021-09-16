import random
import string
import json
import sys
import os
import pathlib

sys.path.append('../')
from bigbreaker.common.tools_identity import ToolsIdentity


with open('config.cfg', 'r') as file:
    config = json.load(file)

id_identity = 'identity_4'
ToolsIdentity.identity_create(config, id_identity)