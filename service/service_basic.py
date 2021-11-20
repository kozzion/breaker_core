import sys
import os
import json

from pathlib import Path


from breaker_core.datasource.jsonqueue import Jsonqueue
from breaker_core.datasource.bytessource import Bytessource
from breaker_core.common.service_jsonqueue import ServiceJsonqueue

class ServiceBasic(ServiceJsonqueue):

    def __init__(self, config_breaker:dict, queue_request, mode_debug) -> None:
        super().__init__(config_breaker, queue_request, mode_debug)

    def process_request(self, request:dict) -> 'dict':
        type_request = request['type_request']
        if type_request == 'copy':
            print('copy')
            sys.stdout.flush()

            bytessource_source = Bytessource.from_dict(self.config_breaker, request['bytessource_source'])
            bytessource_target = Bytessource.from_dict(self.config_breaker, request['bytessource_target'])

            bytessource_target.write(bytessource_source.read())
            
            return {'was_processed':True}
        else:
            return {'was_processed':False, 'message':'Unknown type_request: ' + type_request}



if __name__ == '__main__':
    path_file_config_breaker = Path(os.getenv('PATH_FILE_CONFIG_BREAKER', '/config/config.cfg'))
    path_dir_data =  Path(os.getenv('PATH_DIR_DATA_BREAKER', '/data/data_breaker/' ))
    print(os.getenv('MODE_DEBUG', 'False'))
    mode_debug = os.getenv('MODE_DEBUG', 'False') == 'True'
    print(mode_debug)
    with open(path_file_config_breaker, 'r') as file:
        config_breaker = json.load(file)

    jsonqueue_request = Jsonqueue.from_dict(config_breaker, config_breaker['queue_request_basic_v1'])
    if not jsonqueue_request.exists():
        jsonqueue_request.create()

    service = ServiceBasic(config_breaker, jsonqueue_request, mode_debug)  
    service.run()