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

    def dequeue_blocking(self, timeout_ms:int) -> 'dict':
        raise NotImplementedError()

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
        else:
            raise Exception('incorrect_dict_type')