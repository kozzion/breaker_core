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

list_jobitem = Jobitem.jobitem_load_list(config)

print(len(list_jobitem))
for jobitem in list_jobitem:
    if not 'url_linkedin' in jobitem:
        exit()
    if (not 'want_top_apply'in jobitem) or (jobitem['want_top_apply'] == '?'):
        print(jobitem['want_top_apply'])
        print(jobitem['name_company'])
        print(jobitem['title'])
        list_part = jobitem['description'].split('\n')
        for part in list_part[0:3]:
            print(part.encode('ascii', 'ignore').decode('ascii'))
        promt = ''
        while not promt in ['y','n','?']:
            print('y/n/?')
            promt = input()  
        jobitem['want_top_apply'] = promt
        Jobitem.jobitem_save(config, jobitem['id_jobitem'], jobitem)
        
        # print(jobitem['description'].encode('utf-8'))
        # promt = input()
    
    # querry ='site:www.linkedin.com/jobs'
    # title = jobitem['title']
    # if ',' in title:
    #     title = title.split(',')[0].strip()
    # querry += ' ' + title
    # querry += ' ' + jobitem['name_company']
    # print(querry)
    # url_linkedin = tab_manager_google.action_get_url_first_hit(querry)
    # print(url_linkedin)  
    # exit()
    # jobitem['want_top_apply'] = 'yes'
    # jobitem['has_applied'] = 'yes'
    # Jobitem.jobitem_save(config, jobitem['id_jobitem'], jobitem)
    
  
