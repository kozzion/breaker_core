import json
import hashlib
import pickle
import sys
import tempfile
from pathlib import Path
from typing import List

class Bytessource(object):

    def __init__(self, config:dict) -> None:
        super().__init__()
        self.config = config

    def exists(self) -> bool:
        raise NotImplementedError()

    def read(self) -> 'bytes':
        raise NotImplementedError()

    def write(self, bytes:bytes) -> None:
        raise NotImplementedError()

    def read_json(self) -> 'dict':
        return json.loads(self.read().decode(encoding='utf-8'))

    def read_tempfile(self, suffix='.tmp') -> 'Path':
        path_file = None
        with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as file:
            file.write(self.read())
            path_file = Path(file.name)
        return path_file
        
    def write_json(self, dict_object:'dict') -> 'dict':
        return self.write(json.dumps(dict_object).encode('utf-8'))

    def read_pickle(self) -> 'dict':
        return pickle.loads(self.read())

    def write_pickle(self, dict_object:'dict') -> 'dict':
        return self.write(pickle.dumps(dict_object))

    def delete(self) -> None:
        raise NotImplementedError()

    def size(self):
        raise NotImplementedError()

    def list_shallow(self):        
        raise NotImplementedError()

    def list_deep(self):
        raise NotImplementedError()

    @staticmethod
    def list_list_key_to_dict_hierarchy(list_list_key):
        dict_root = {}
        for list_key in list_list_key:
            dict = dict_root
            for key in list_key:
                if not key in dict:
                    dict[key] = {}
                dict = dict[key]
        return dict_root

    @staticmethod
    def list_list_key_to_dict_hash(list_list_key):
        dict_hash = {}
        for list_key in list_list_key:
            name_object = '/'.join(list_key)
            hash_object = hashlib.sha256(name_object.encode('utf-8')).hexdigest()
            dict_hash[hash_object] = list_key
        return dict_hash

    

    def sync_to(self, other:'Bytessource', delete_missing:bool=False) -> None:
        dict_self = Bytessource.list_list_key_to_dict_hash(self.list_deep())
        dict_other = Bytessource.list_list_key_to_dict_hash(other.list_deep())
        for hash_object in dict_self:
            child_self = self.join(dict_self[hash_object])
            child_other = other.join(dict_self[hash_object])
            if not hash_object in dict_other:                
                child_other.write(child_self.read())
                print('write:')
            else:
                print('update todo')
                del dict_other[hash_object]
            sys.stdout.flush()

        if delete_missing:
            for hash_object in dict_other:
                other.join(dict_other[hash_object]).delete()
                print('delete')
                sys.stdout.flush()
                

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
    def from_dict(config, dict_bytessource) -> 'Bytessource':
        type_bytessource = dict_bytessource['type_bytessource']
        if type_bytessource == 'BytessourceFile':
            from breaker_core.datasource.bytessource_file import BytessourceFile
            return BytessourceFile.from_dict(config, dict_bytessource)
        elif type_bytessource == 'BytessourceCallback':
            from breaker_core.datasource.bytessource_callback import BytessourceCallback
            return BytessourceCallback.from_dict(config, dict_bytessource)
        elif type_bytessource == 'BytessourceS3':
            from breaker_aws.datasource.bytessource_s3 import BytessourceS3
            return BytessourceS3.from_dict(config, dict_bytessource)
        else:
            raise Exception('Uknown type_bytessource: ' + type_bytessource)

    def __str__(self):
        return str(self.to_dict())

   

  