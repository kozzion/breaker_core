import sys
import os
import json



sys.path.append('../')
from breaker_core.builtin.jobitem import Jobitem


with open('config.cfg', 'r') as file:
    config = json.load(file)
path_dir_data = config['path_dir_data']

id_jobitem = '15785'




# list_sector = Jobitem.sector_load_list()
# list_sector = Jobitem.sector_save()



sector = 'hospitality'

Jobitem.generate_cover_letter(config, id_jobitem)
print(Jobitem.coverletterpdf_load_path(config, id_jobitem))