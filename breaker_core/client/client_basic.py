import sys
import time

from breaker_core.tools_general import ToolsGeneral
from breaker_core.datasource.jsonqueue import Jsonqueue
from breaker_core.datasource.bytessource import Bytessource

class ClientBasic(object):

    def __init__(
        self,
        jsonqueue_request:Jsonqueue) -> None:
        super(ClientBasic, self).__init__()
        self.jsonqueue_request = jsonqueue_request

    def request_copy(self, bytessource_source:Bytessource, bytessource_target:Bytessource, bytessource_response:Bytessource):
        dict_request_payload = {}
        dict_request_payload['type_request'] = 'copy'
        dict_request_payload['bytessource_source'] = bytessource_source.to_dict()
        dict_request_payload['bytessource_target'] = bytessource_target.to_dict()
 
        dict_request = {}
        dict_request['payload_request'] = dict_request_payload
        dict_request['bytessource_response'] = bytessource_response.to_dict()

        self.jsonqueue_request.enqueue(dict_request)

