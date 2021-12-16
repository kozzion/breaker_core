import time

class Jsonqueue:

    def __init__(self, config:dict) -> None:
        super().__init__()
        self.config = config

    # def capacity(self) -> int:
    #     raise NotImplementedError()

    # def count(self) -> int:
    #     raise NotImplementedError()

    def dequeue(self) -> 'dict':
        raise NotImplementedError()

    def dequeue_blocking(self, timeout_ms:int=5000, *, sleep_increment_ms:int=5000) -> dict:
        while True:
            dict_json = self.dequeue()
            if not dict_json is None:
                return dict_json
            elif timeout_ms == -1:
                continue
            elif timeout_ms == 0:
                return None
            elif (timeout_ms <= sleep_increment_ms):
                time.sleep(timeout_ms / 1000)
                timeout_ms = 0
            else:
                time.sleep(sleep_increment_ms / 1000)
                timeout_ms -= sleep_increment_ms

    def enqueue(self, dict:'dict') -> None:
        raise NotImplementedError()

    def to_dict(self):
        raise NotImplementedError()

    @staticmethod
    def from_dict(config:'dict', dict_jsonqueue:'dict') -> 'Jsonqueue':
        if dict_jsonqueue['type_jsonqueue'] == 'JsonqueueFile':
            from breaker_core.datasource.jsonqueue_file import JsonqueueFile
            return JsonqueueFile.from_dict(config, dict_jsonqueue)
        elif dict_jsonqueue['type_jsonqueue'] == 'JsonqueueSqs':
            from breaker_aws.datasource.jsonqueue_sqs import JsonqueueSqs
            return JsonqueueSqs.from_dict(config, dict_jsonqueue)
        elif dict_jsonqueue['type_jsonqueue'] == 'JsonqueueS3':
            from breaker_aws.datasource.jsonqueue_s3 import JsonqueueS3
            return JsonqueueS3.from_dict(config, dict_jsonqueue)
        else:
            raise Exception('Unknown Jsonqueue type: ' + dict_jsonqueue['type_jsonqueue'])