import os
import sys
import json
import pickle as pkl
class LinkedinPerson:
            
    def linkedin_person_save_pkl(config, id_linkedin_person, linkedin_person):
        path_dir_data = config['path_dir_data']  
        path_dir_linkedin_person = os.path.join(path_dir_data, 'linkedin', 'person', id_linkedin_person)
        path_file_linkedin_person = os.path.join(path_dir_data, 'linkedin', 'person', id_linkedin_person, 'linkedin_person.pkl')

        if not os.path.isdir(path_dir_linkedin_person):
            os.makedirs(path_dir_linkedin_person)
        
        driver = linkedin_person.driver
        linkedin_person.driver = None
        with open(path_file_linkedin_person, 'wb') as file:
            pkl.dump(linkedin_person, file)
        linkedin_person.driver = driver

    def linkedin_person_has_pkl(config, id_linkedin_person):
        path_dir_data = config['path_dir_data']  
        path_file_linkedin_person = os.path.join(path_dir_data, 'linkedin', 'person', id_linkedin_person, 'linkedin_person.pkl')
        return os.path.isfile(path_file_linkedin_person)

    def linkedin_person_load_pkl(config, id_linkedin_person):
        path_dir_data = config['path_dir_data']  
        path_file_linkedin_person = os.path.join(path_dir_data, 'linkedin', 'person', id_linkedin_person, 'linkedin_person.pkl')
        with open(path_file_linkedin_person, 'rb') as file:
            return pkl.load(file)