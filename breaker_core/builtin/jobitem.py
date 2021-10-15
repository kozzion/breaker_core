
import os
import sys
import json
import time
from datetime import date
from docx2pdf import convert
import zipfile

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

        if not 'list_status' in jobitem:
            timestamp = int(time.time())
            jobitem['list_status'] = [{'timestamp':timestamp, 'message':jobitem['status_apply'] }]
        Jobitem.jobitem_save(config, jobitem['id_jobitem'], jobitem)
        return jobitem

    @staticmethod
    def jobitem_create(config, id_jobitem, ):
        path_dir_data = config['path_dir_data']  
        path_dir_jobitem = os.path.join(path_dir_data, 'builtin', 'jobitem', id_jobitem)
        path_file_jobitem = os.path.join(path_dir_data, 'builtin', 'jobitem', id_jobitem, 'jobitem.json')
        if not os.path.isdir(path_dir_jobitem):
            os.makedirs(path_dir_jobitem)
        jobitem = {}
        jobitem['list_status'] = []

        timestamp = int(time.time())
        jobitem['list_status'].append({'timestamp':timestamp,'message':'application_scaped'})
        with open(path_file_jobitem, 'w') as file:
            json.dump(jobitem, file)

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
    def jobitem_status_update(config, id_jobitem, message_status):
        jobitem = Jobitem.jobitem_load(config, id_jobitem)
        timestamp = int(time.time())
        jobitem['list_status'].append({'timestamp':timestamp,'message':message_status})
        Jobitem.jobitem_save(config, id_jobitem, jobitem)


    @staticmethod
    def jobitem_status_message(config, id_jobitem):
        jobitem = Jobitem.jobitem_load(config, id_jobitem)
        return jobitem['list_status'][-1]['message']

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
    
    @staticmethod
    def coverletterdocx_load_path(config, id_jobitem):
        path_dir_data = config['path_dir_data']  
        return os.path.join(path_dir_data, 'builtin', 'jobitem', id_jobitem, 'cover_letter.docx')
            
    @staticmethod
    def coverletterpdf_load_path(config, id_jobitem):
        path_dir_data = config['path_dir_data']  
        return os.path.join(path_dir_data, 'builtin', 'jobitem', id_jobitem, 'cover_letter.pdf')


    @staticmethod
    def docx_replace(path_file_docx_source, path_file_docx_target, dict_replace):
        zipfile_source = zipfile.ZipFile(path_file_docx_source, 'r')
        zipfile_target = zipfile.ZipFile(path_file_docx_target, 'w')
        for item in zipfile_source.infolist():
            buffer = zipfile_source.read(item.filename)
            if (item.filename == 'word/document.xml'):
                text = buffer.decode("utf-8")
                # index_end = 0
                # list_part = []
                # while True:
                #     index_start = text.find('<w:t>', index_end + 1)
                #     index_end = text.find('</w:t>', index_end + 1)
                #     if index_end == -1:
                #         break 
                #     else:
                        
                #         part = text[index_start + 5: index_end]
                #         list_part.append(part)
                #         if 0 < len(part.strip()): 
                #             print(part)

                for text_replace in dict_replace:
                     
                    count_replace = dict_replace[text_replace][0]
                    text_replace_with = dict_replace[text_replace][1]
                    if text.count(text_replace) != count_replace:

                        with open('xml.txt', 'w') as file:
                            file.write(text)

                        raise Exception('replacement count incorrect for: "' + text_replace  + '" expected ' + str(count_replace) + ' found ' + str(text.count(text_replace)))
                    else:
                        text = text.replace(text_replace, text_replace_with)
                buffer = text.encode("utf-8")
            zipfile_target.writestr(item, buffer)
        zipfile_target.close()
        zipfile_source.close()


    @staticmethod
    def generate_cover_letter(config, jobitem, identity):
        path_dir_data = config['path_dir_data']  
        path_file_docx_source = os.path.join(path_dir_data, 'cover_letter.docx')
        id_jobitem = jobitem['id_jobitem']

        jobitem = Jobitem.jobitem_load(config, id_jobitem)
        path_file_docx_target = Jobitem.coverletterdocx_load_path(config, id_jobitem)
        path_file_pdf = Jobitem.coverletterpdf_load_path(config, id_jobitem)

        # list_sector = Jobitem.sector_load_list()
        # list_sector = Jobitem.sector_save()
        # print(jobitem)
        #sector = 'hospitality'


        title = jobitem['title']
        if ' OR ' in title:
            title = title.split(' OR ')[0]

        dict_replace = {}
        dict_replace['#'] = (1, date.today().strftime('%B %d %Y'))
        dict_replace['$'] = (1, jobitem['name_company'])
        dict_replace['^'] = (2, title)
        #dict_replace['*'] = (0, sector)

        Jobitem.docx_replace(path_file_docx_source, path_file_docx_target, dict_replace)
        convert(path_file_docx_target, path_file_pdf)