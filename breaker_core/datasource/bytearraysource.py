

class Bytearraysource:

    def __init__(self) -> None:
        pass

    def exists(self) -> bool:
        raise NotImplementedError()

    def save(self, bytearray:bytearray) -> None:
        raise NotImplementedError()

    def load(self) -> bytearray:
        raise NotImplementedError()

    def delete(self) -> None:
        raise NotImplementedError()

    def to_dict(self):
        raise NotImplementedError()

    @staticmethod
    def from_dict(dict_bytearraysource):
        if dict_bytearraysource['type_bytearraysource'] == 'BytearraysourceFile':
            from breaker_core.datasource.bytearraysource_file import BytearraysourceFile
            return BytearraysourceFile.from_dict(dict_bytearraysource)
        elif dict_bytearraysource['type_bytearraysource'] == 'BytearraysourceS3':
            from breaker_aws.datasource.bytearraysource_s3 import BytearraysourceS3
            return BytearraysourceS3.from_dict(dict_bytearraysource)
        else:
            raise Exception('incorrect_dict_type')