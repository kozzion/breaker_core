import json
import pickle
from typing import List
from pathlib import Path
class Bytessource(object):

    def __init__(self) -> None:
        pass

    def exists(self) -> bool:
        raise NotImplementedError()

    def read(self) -> 'bytes':
        raise NotImplementedError()

    def write(self, bytes:bytes) -> None:
        raise NotImplementedError()

    def read_json(self) -> 'dict':
        return json.loads(self.read().decode(encoding='utf-8'))

    def write_json(self, dict_object:'dict') -> 'dict':
        return self.write(json.dumps(dict_object).encode('utf-8'))

    def read_pickle(self) -> 'dict':
        #todo simplyfy
        path_file_temp = Path('temp')
        path_file_temp.write_bytes(self.read())
        with open(path_file_temp, 'rb') as file:
            return pickle.load(file)

    def write_pickle(self, dict_object:'dict') -> 'dict':
        return self.write(pickle.dumps(dict_object))

    def delete(self) -> None:
        raise NotImplementedError()

    def size(self):
        raise NotImplementedError()

    def list_shallow(self):        
        raise NotImplementedError()

    def validate_list_key(self, list_key:List[str]):
            if not isinstance(list_key, list):
                    raise RuntimeError('list_key must be list')
            list_str_forbidden = []
            for key in list_key:
                if not isinstance(key, str):
                    raise RuntimeError('key must be string')
                for str_forbidden in list_str_forbidden:
                    if str_forbidden in key:
                        raise RuntimeError('keys cannot contain "' + str_forbidden + '"')


    def join(self, list_key:List[str]) -> 'Bytessource':
         raise NotImplementedError()

    def join_last(self, mode='str'):
        list_list_key = self.list_shallow()
        if len(list_list_key) == 0:
            return None
            
        list_key = [list_key[0] for list_key in list_list_key]
        if mode == 'str':
            key = sorted(list_key)[-1]
        else:
            raise NotImplementedError()
        return self.join([key])

    def list_for_prefix(self, list_key_prefix:List[str]) -> 'List[List[str]]':
        raise NotImplementedError()

    def to_dict(self):
        raise NotImplementedError()
  
    @staticmethod
    def from_dict(dict_bytessource) -> 'Bytessource':
        type_bytessource = dict_bytessource['type_bytessource']
        if type_bytessource == 'BytessourceFile':
            from breaker_core.datasource.bytessource_file import BytessourceFile
            return BytessourceFile.from_dict(dict_bytessource)
        elif type_bytessource == 'BytessourceS3':
            from breaker_aws.datasource.bytessource_s3 import BytessourceS3
            return BytessourceS3.from_dict(dict_bytessource)
        else:
            raise Exception('incorrect_dict_type: ' + type_bytessource)



   

  