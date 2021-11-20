import sys
import time

from breaker_core.tools_general import ToolsGeneral
from breaker_core.datasource.jsonqueue import Jsonqueue
from breaker_core.datasource.bytessource import Bytessource

class ClientJsonqueue(object):

    def __init__(
        self,
        jsonqueue_request:Jsonqueue,
        bytessource_response:Bytessource) -> None:
        super(ClientJsonqueue, self).__init__()
        self.jsonqueue_request = jsonqueue_request
        self.bytessource_response = bytessource_response
        #TODO add option for a status file


    def await_response(self, dict_request_payload:dict, force_reprocess:bool=False):
        hash_request = ToolsGeneral.sha256_dict_json(dict_request_payload)
        print(hash_request)
        dict_request = {}
        dict_request['payload_request'] = dict_request_payload
        bytessource_response = self.bytessource_response.join([hash_request])
        dict_request['bytessource_response'] = bytessource_response.to_dict()

        if bytessource_response.exists() and force_reprocess:
            bytessource_response.delete()
        
        if bytessource_response.exists():
            print('response found')
            sys.stdout.flush()
            return bytessource_response.read_json()
        else:
            print('writing request')
            sys.stdout.flush()
            self.jsonqueue_request.enqueue(dict_request)

            while(True):
                if bytessource_response.exists():
                    time.sleep(0.001)
                    return bytessource_response.read_json()
                else:
                    time.sleep(0.1)

