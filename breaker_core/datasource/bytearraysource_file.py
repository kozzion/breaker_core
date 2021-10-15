import os

from pathlib import Path

from breaker_core.datasource.bytearraysource import Bytearraysource

class BytearraysourceFile(Bytearraysource):

    def __init__(self, path_file:Path) -> None:
        self.path_file = path_file

    def exists(self) -> bool:
        return self.path_file.exists()

    def save(self, bytearray_object:bytearray) -> None:
        if not self.path_file.parent.is_dir():
            os.makedirs(self.path_file.parent, exist_ok=True)

        with open(self.path_file, 'wb') as file:
            file.write(bytearray_object)

    def load(self) -> bytearray:
        with open(self.path_file, 'rb') as file:
            return file.read()

    def delete(self) -> None:
        if self.path_file.is_file():
            os.remove(self.path_file)
            
    def to_dict(self):
        dict_bytearraysource = {}
        dict_bytearraysource['type_bytearraysource'] = 'BytearraysourceFile'
        dict_bytearraysource['path_file'] = str(self.path_file.absolute())
        return dict_bytearraysource

    @staticmethod
    def from_dict(dict_bytearraysource):
        if not dict_bytearraysource['type_bytearraysource'] == 'BytearraysourceFile':
            raise Exception('incorrect_dict_type')
        return BytearraysourceFile(Path(dict_bytearraysource['path_file']))

