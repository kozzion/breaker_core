import sys
import time

from breaker_core.datasource.jsonqueue import Jsonqueue
from breaker_core.datasource.bytessource import Bytessource

class ServiceJsonqueue(object):

    def __init__(self, config_breaker:dict, queue_request:Jsonqueue, mode_debug:bool) -> None:
        super().__init__()
        self.config_breaker = config_breaker
        self.queue_request = queue_request
        self.mode_debug = mode_debug

    def run(self):
        count_sleep = 0
        while True:
            dict_request = self.queue_request.dequeue_blocking(timeout_ms=5000)
            while dict_request == None:
                count_sleep += 1
                print('sleep ' + str(count_sleep))
                sys.stdout.flush()
                dict_request = self.queue_request.dequeue_blocking(timeout_ms=5000)


            try:
                bytessource_update = Bytessource.from_dict(self.config_breaker, dict_request['bytessource_update'])
            except Exception as e:
                print('Exception while reading bytessource_update: ' +  str(e))
                sys.stdout.flush()
                if self.mode_debug:
                    print('mode_debug')
                    raise e
             

            try:
                self.process_request(dict_request)
            except Exception as e:

                print('Exception while processing request: ' + str(e))
                bytessource_update.write_json(
                    {
                        'status':'failed',
                        'message':'Exception while processing request: ' + str(e),              
                })
                if self.mode_debug:
                    print('mode_debug')
                    raise e

   


    def process_request(self, request:dict) -> 'dict':
        raise NotImplementedError()