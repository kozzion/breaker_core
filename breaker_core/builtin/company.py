
import os
import sys
import json

class Company:

    @staticmethod
    def company_save(config, id_company, json_company):
        path_dir_data = config['path_dir_data']  
        path_file_company = os.path.join(path_dir_data, 'builtin', 'company', id_company, 'company.json')
        with open(path_file_company, 'w') as file:
            json.dump(json_company, file)

    @staticmethod
    def company_load(config, id_company):
        path_dir_data = config['path_dir_data']  
        path_file_company = os.path.join(path_dir_data, 'builtin', 'company', id_company, 'company.json')
        with open(path_file_company, 'r') as file:
            return json.load(file)

            