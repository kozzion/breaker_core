import os
import sys
import json
import random
import string

from bigbreaker.common.system_webdriver import SystemWebdriver

class ToolsIdentity:

    def identity_create(config, id_identity, random_seed = None):
        path_dir_data = config['path_dir_data']
        path_dir_identity = os.path.join(path_dir_data, 'identity', id_identity)
        if not os.path.isdir(path_dir_identity):
            os.makedirs(path_dir_identity)

        path_file_identity = os.path.join(path_dir_data, 'identity', id_identity, 'identity.json')
        if os.path.isfile(path_file_identity):
            raise Exception('exists')

        path_file_list_name_first = os.path.join(path_dir_data, 'list_first_name.txt')
        path_file_list_name_last = os.path.join(path_dir_data, 'list_first_name.txt')
        

       


        size_password = 12
        with open(path_file_list_name_first, encoding='ascii', errors='ignore') as file:
            list_name_first = file.readlines()
        with open(path_file_list_name_last, encoding='ascii', errors='ignore') as file:
            list_name_last = file.readlines()
        if random_seed:
            random.random.seed = random_seed

        identity = {}
        identity['id_identity'] = id_identity
        identity['name_first_0']  = random.choice(list_name_first).strip()
        identity['name_last_0']   = random.choice(list_name_last).strip()
        identity["name_full"]  = identity["name_first_0"] + " " + identity["name_last_0"]
        
        identity["birthday_year"] = random.randint(1974, 1999)
        identity["birthday_month"] = random.randint(1, 12)
        identity["birthday_day"]  = random.randint(1, 28)
        
        
        identity['onionmail_username'] = ''.join(random.choices(string.ascii_lowercase + string.ascii_uppercase + string.digits, k=size_password))
        identity['onionmail_address']  = identity['onionmail_username'] + '@onionmail.org'
        identity['onionmail_password'] = ''.join(random.choices(string.ascii_lowercase + string.ascii_uppercase + string.digits, k=size_password))
        identity['onionmail_is_created'] = False

        identity['instagram_username'] = identity['name_first_0'] + ''.join(random.choices(string.ascii_lowercase + string.ascii_uppercase + string.digits, k=6))
        identity['instagram_password'] = ''.join(random.choices(string.digits + string.ascii_uppercase + string.digits, k=4))
        identity['instagram_is_created'] = False

        identity['linkedin_username'] = identity['name_first_0'] + '_' + identity['name_last_0'] + ''.join(random.choices(string.digits, k=4))
        identity['linkedin_password'] = ''.join(random.choices(string.ascii_lowercase + string.ascii_uppercase + string.digits, k=size_password))
        identity['linkedin_is_created'] = False
        
        identity['gmail_username'] = identity['name_first_0'] + '_' + identity['name_last_0'] + ''.join(random.choices(string.digits, k=6))
        identity['gmail_password'] = ''.join(random.choices(string.ascii_lowercase + string.ascii_uppercase + string.digits, k=size_password))
        identity['gmail_is_created'] = False
        
        with open(path_file_identity, 'w') as file:
            json.dump(identity, file)

        return identity

    def identity_load(config, id_identity):
        path_dir_data = config['path_dir_data']
        path_file_identity = os.path.join(path_dir_data, 'identity', id_identity, 'identity.json')
        with open(path_file_identity, 'r') as file:
            return json.load(file)

    def identity_has(config, id_identity):
        path_dir_data = config['path_dir_data']
        path_file_identity = os.path.join(path_dir_data, 'identity', id_identity, 'identity.json')
        return os.path.isfile(path_file_identity)

    def identity_save(config, id_identity, identity):
        if not identity['id_identity'] == id_identity:
            raise Exception()

        path_dir_data = config['path_dir_data']
        path_file_identity = os.path.join(path_dir_data, 'identity', id_identity, 'identity.json')
        with open(path_file_identity, 'w') as file:
            json.dump(identity, file)

    def webdriver_load(config, id_identity):
        path_dir_data = config['path_dir_data']
        path_file_webdriver = config['path_file_webdriver']
        path_file_session = os.path.join(path_dir_data, 'identity', id_identity, 'session.json')
        path_dir_user_data = os.path.join(path_dir_data, 'identity', id_identity, 'selenium')
        system_webdriver = SystemWebdriver(path_file_webdriver)
        return system_webdriver.get_webdriver(path_file_session, path_dir_user_data)
        
