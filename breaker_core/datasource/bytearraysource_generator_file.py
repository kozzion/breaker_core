import os

from pathlib import Path

from breaker_core.datasource.bytearraysource_generator import BytearraysourceGenerator
from breaker_core.datasource.bytearraysource import Bytearraysource
from breaker_core.datasource.bytearraysource_file import BytearraysourceFile


class BytearraysourceGeneratorFile(BytearraysourceGenerator):

    def __init__(self, path_dir_root:Path) -> None:
        self.path_dir_root = path_dir_root

    def generate(self, list_key:list[str]) -> Bytearraysource:
        self.validate_list_key(list_key)
        path = self.path_dir_root
        for key in list_key:
            path = path.joinpath(key)
        return BytearraysourceFile(path)


    def list_for_prefix(self, list_key_prefix:list[str]) -> list[list[str]]:
        self.validate_list_key(list_key_prefix)
        path = self.path_dir_root
        for key in list_key_prefix:
            path = path.joinpath(key)

        if path.is_dir():
            list_list_key = []
            for name_file in os.listdir(path):
                list_key = list_key_prefix.copy()
                list_key.append(name_file)
                list_list_key.append(list_key)
                #TODO also go down directories
            return list_list_key

        elif path.is_file():
            list_key = list_key_prefix.copy()
            list_key.append(path.name)
            return [list_key]

        else:
            return []
            #do partial matches here
            raise NotImplementedError()
       
        #TODO alse find files starting with the last key in the second to last dir

    def to_dict(self):
        dict_bytearraysource = {}
        dict_bytearraysource['type_bytearraysource'] = 'BytearraysourceGeneratorFile'
        dict_bytearraysource['path_dir_root'] = str(self.path_dir_root.absolute())
        return dict_bytearraysource

    @staticmethod
    def from_dict(dict_bytearraysource):
        if not dict_bytearraysource['type_bytearraysource'] == 'BytearraysourceGeneratorFile':
            raise Exception('incorrect_dict_type')
        return BytearraysourceGeneratorFile(Path(dict_bytearraysource['path_dir_root']))