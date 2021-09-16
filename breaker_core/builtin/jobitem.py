
import os
import sys
import json

class Jobitem:

    @staticmethod
    def jobitem_validate(config, jobitem):
        if not 'status_apply' in jobitem:
            if jobitem['has_applied'] == "y":
                jobitem['status_apply'] = 'has_applied'
            elif (jobitem['want_top_apply'] == "y"):
                jobitem['status_apply'] = 'want_top_apply' 
            else:
                jobitem['status_apply'] = 'gathered'
        Jobitem.jobitem_save(config, jobitem['id_jobitem'], jobitem)
        return jobitem

    @staticmethod
    def jobitem_save(config, id_jobitem, json_jobitem):
        path_dir_data = config['path_dir_data']  
        path_dir_jobitem = os.path.join(path_dir_data, 'builtin', 'jobitem', id_jobitem)
        path_file_jobitem = os.path.join(path_dir_data, 'builtin', 'jobitem', id_jobitem, 'jobitem.json')
        if not os.path.isdir(path_dir_jobitem):
            os.makedirs(path_dir_jobitem)
        with open(path_file_jobitem, 'w') as file:
            json.dump(json_jobitem, file)

    @staticmethod
    def jobitem_load(config, id_jobitem):
        path_dir_data = config['path_dir_data']  
        path_file_jobitem = os.path.join(path_dir_data, 'builtin', 'jobitem', id_jobitem, 'jobitem.json')
        with open(path_file_jobitem, 'r') as file:
            return json.load(file)

    @staticmethod        
    def jobitem_load_list(config):
        path_dir_data = config['path_dir_data']  
        path_dir_jobitem = os.path.join(path_dir_data, 'builtin', 'jobitem')
        list_id_jobitem = os.listdir(path_dir_jobitem)
        list_jobitem = []
        for id_jobitem in list_id_jobitem:
            list_jobitem.append(Jobitem.jobitem_load(config, id_jobitem))
        return list_jobitem