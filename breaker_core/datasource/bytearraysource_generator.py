from breaker_core.datasource.bytearraysource import Bytearraysource

class BytearraysourceGenerator:

    def __init__(self) -> None:
        pass
    
    def validate_list_key(self, list_key:list[str]):
        if not isinstance(list_key, list):
                raise RuntimeError('list_key must be list')
        list_str_forbidden = []
        for key in list_key:
            if not isinstance(key, str):
                 raise RuntimeError('key must be string')
            for str_forbidden in list_str_forbidden:
                if str_forbidden in key:
                    raise RuntimeError('keys cannot contain "' + str_forbidden + '"')

    def generate(self, list_key:list[str]) -> Bytearraysource:
        raise NotImplementedError()

    def list_for_prefix(self, list_key_prefix:list[str]) -> list[list[str]]:
        raise NotImplementedError()

    def to_dict(self):
        raise NotImplementedError()
        
    @staticmethod
    def from_dict(dict_bytearraysource):
        if dict_bytearraysource['type_bytearraysource'] == 'BytearraysourceGeneratorFile':
            from breaker_core.datasource.bytearraysource_generator_file import BytearraysourceGeneratorFile
            return BytearraysourceGeneratorFile.from_dict(dict_bytearraysource)
        if dict_bytearraysource['type_bytearraysource'] == 'BytearraysourceGeneratorS3':
            from breaker_aws.datasource.bytearraysource_generator_s3 import BytearraysourceGeneratorS3
            return BytearraysourceGeneratorS3.from_dict(dict_bytearraysource)