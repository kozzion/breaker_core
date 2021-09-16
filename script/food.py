import sys
import os
import json

from docx2pdf import convert
import zipfile
from datetime import date

sys.path.append('../')
from bigbreaker.builtin.jobitem import Jobitem


with open('config.cfg', 'r') as file:
    config = json.load(file)
path_dir_data = config['path_dir_data']

id_jobitem = '15785'


path_file_docx_source = os.path.join(path_dir_data, 'cover_letter.docx')


# @staticmethod
def coverletterdocx_load_path(config, id_jobitem):
    path_dir_data = config['path_dir_data']  
    return os.path.join(path_dir_data, 'builtin', 'jobitem', id_jobitem, 'cover_letter.docx')
        
# @staticmethod
def coverletterpdf_load_path(config, id_jobitem):
    path_dir_data = config['path_dir_data']  
    return os.path.join(path_dir_data, 'builtin', 'jobitem', id_jobitem, 'cover_letter.pdf')



def docx_replace(path_file_docx_source, path_file_docx_target, dict_replace):
    zipfile_source = zipfile.ZipFile(path_file_docx_source, 'r')
    zipfile_target = zipfile.ZipFile(path_file_docx_target, 'w')
    for item in zipfile_source.infolist():
        buffer = zipfile_source.read(item.filename)
        if (item.filename == 'word/document.xml'):
            text = buffer.decode("utf-8")
            print(text)
            for replace in dict_replace:
                if not replace in text:
                    print('not found: ' + replace)
                    if not replace[1:] in text:
                        print('not found: ' + replace[1:])
                else:
                    text = text.replace(replace, dict_replace[replace])
            buffer = text.encode("utf-8")
        zipfile_target.writestr(item, buffer)
    zipfile_target.close()
    zipfile_source.close()


def promt_option(list_option, ):
    dict_option = {}
    for index_option, option in enumerate(list_option):
        str_index_option = str(index_option + 1)
        dict_option
        print('(' + str_index_option + ') ' + option)
    dict_option['q'] = 'quit'
    prompt = ''
    while prompt not in dict_option:
        prompt = input()
    if dict_option[prompt] == 'quit':
        exit()
    return dict_option[prompt]

jobitem = Jobitem.jobitem_load(config, id_jobitem)
path_file_docx_target = coverletterdocx_load_path(config, id_jobitem)
path_file_pdf = coverletterpdf_load_path(config, id_jobitem)

# list_sector = Jobitem.sector_load_list()
# list_sector = Jobitem.sector_save()
# Jobitem.coverletterdocx_load_path(config, id_jobitem)
# Jobitem.coverletterpdf_load_path(config, id_jobitem)

print(jobitem)
sector = 'hospitality'

dict_replace = {}
dict_replace['DA'] = date.today().strftime('%B %d %Y')
dict_replace['CN'] = jobitem['name_company']
dict_replace['PN'] = jobitem['title']
dict_replace['SE'] = sector


print(dict_replace)



docx_replace(path_file_docx_source, path_file_docx_target, dict_replace)
convert(path_file_docx_target, path_file_pdf)