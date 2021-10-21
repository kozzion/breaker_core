import os
from pathlib import Path
from typing import List
from breaker_core.datasource.bytessource import Bytessource

class BytessourceFile(Bytessource):

    def __init__(self, path_dir_root:Path, list_key:List[str]=[]) -> None:
        super(BytessourceFile, self).__init__()
        self.validate_list_key(list_key)
        self.path_dir_root = path_dir_root
        self.list_key = list_key
        self.path = self.path_dir_root
        for key in list_key:
            self.path = self.path.joinpath(key)

    def exists(self) -> bool:
        return self.path.is_file()

    def write(self, bytearray_object:bytearray) -> None:
        print('here')
        print(self.path)
        if not self.path.parent.is_dir():
            os.makedirs(self.path.parent, exist_ok=True)

        with open(self.path, 'wb') as file:
            file.write(bytearray_object)

    def read(self) -> bytearray:
        with open(self.path, 'rb') as file:
            return file.read()

    def delete(self) -> None:
        if self.path.is_file():
            os.remove(self.path)
            

    def join(self, list_key:List[str]) -> 'Bytessource':
        self.validate_list_key(list_key)
        list_key_extended = self.list_key.copy()
        list_key_extended.extend(list_key)
        return BytessourceFile(self.path_dir_root, list_key_extended)

    def list_shallow(self, prefix='') -> 'List[List[str]]':
        if self.path.is_dir():
            list_list_key = []
            for name_file in os.listdir(self.path):
                if name_file.startswith(prefix):
                    list_list_key.append([name_file])
            return list_list_key
        else:
            return []

    def list_deep(self, prefix='') -> 'List[List[str]]':
        if self.path.is_dir():
            list_list_key = []
            for name_file in os.listdir(self.path):
                if prefix in name_file:
                    list_list_key.append([name_file])
                #TODO also go down directories
            return list_list_key

    def list_for_prefix(self, list_key_prefix:List[str]) -> 'List[List[str]]':
        self.validate_list_key(list_key_prefix)
        path = self.path
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



    def to_dict(self) -> 'dict':
        dict_bytessource = {}
        dict_bytessource['type_bytessource'] = 'BytessourceFile'
        dict_bytessource['path_dir_root'] = str(self.path_dir_root.absolute())
        dict_bytessource['list_key'] = self.list_key 
        return dict_bytessource

    @staticmethod
    def from_dict(dict_bytessource) -> 'Bytessource':
        if not dict_bytessource['type_bytessource'] == 'BytessourceFile':
            raise Exception('incorrect_dict_type')
        return BytessourceFile(Path(dict_bytessource['path_dir_root']), dict_bytessource['list_key'])

