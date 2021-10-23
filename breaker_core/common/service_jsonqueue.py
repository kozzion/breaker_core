import sys
import time

from breaker_core.datasource.jsonqueue import Jsonqueue
from breaker_core.datasource.bytessource import Bytessource

class ServiceJsonqueue(object):

    def __init__(self, queue_request:Jsonqueue, mode_debug:bool) -> None:
        super().__init__()
        self.queue_request = queue_request
        self.mode_debug = mode_debug

    def run(self):
        count_sleep = 0
        while True:
            dict_request = self.queue_request.dequeue()
            while dict_request == None:
                count_sleep += 1
                dict_request = self.queue_request.dequeue()
                time.sleep(0.1)
                if count_sleep % 10 == 0:
                    print('sleep ' + str(count_sleep))
                    sys.stdout.flush()


            try:
                bytessource_response = Bytessource.from_dict(dict_request['bytessource_response'])
            except Exception as e:
                print('Exception while reading request: ' +  str(e))
                sys.stdout.flush()
                if self.mode_debug:
                    raise e
             



            try:
                response = self.process_request(dict_request['payload_request'])
            except Exception as e:

                print('Exception while processing request: ' + str(e))
                bytessource_response.write_json(
                    {
                        'was_processed':False,
                        'message':'Exception while processing request: ' + str(e)
                })
                if self.mode_debug:
                    raise e


            try:
      
                bytessource_response.write_json(response)
            except Exception as e:
                print('Exception writing response ' + str(e))
                sys.stdout.flush()
                if self.mode_debug:
                    raise e

   


    def process_request(self, request:dict) -> 'dict':
        raise NotImplementedError()