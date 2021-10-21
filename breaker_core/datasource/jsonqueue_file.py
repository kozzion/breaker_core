import os
import json
import time
import random
import string

from pathlib import Path

from breaker_core.datasource.jsonqueue import Jsonqueue

class JsonqueueFile(Jsonqueue):

    def __init__(self, path_dir:Path) -> None:
        self.path_dir = path_dir
        if self.path_dir.is_file():
            raise Exception(self.path_dir + 'is file')

        if not self.path_dir.is_dir():
            os.makedirs(self.path_dir, exist_ok=True)

    def exists(self) -> bool:
        return self.path_dir.is_dir()
    
    def create(self) -> None:
        os.makedirs(self.path_dir)

    def delete(self) -> None:
        os.removedirs(self.path_dir)

    def clear(self) -> None:
        os.removedirs(self.path_dir)
        os.makedirs(self.path_dir)
        
    def dequeue(self) -> dict:
        list_name_file = os.listdir(self.path_dir)
        if len(list_name_file) == 0:
            return None
        name_file = list_name_file[0]
        path_file_json = self.path_dir.joinpath(name_file)
        with path_file_json.open('r', encoding='utf-8') as file:
            dict_json = json.load(file)
        os.remove(path_file_json)
        return dict_json
         
    def dequeue_blocking(self, timeout_ms:int=-1, *, sleep_increment_ms:int=10) -> dict:
        while True:
            dict_json = self.dequeue(self)
            if not dict_json is None:
                return dict_json
            elif timeout_ms == -1:
                continue
            elif timeout_ms == 0:
                return None
            elif (timeout_ms <= sleep_increment_ms):
                timeout_ms = 0
                time.sleep(timeout_ms)
            else:
                timeout_ms -= sleep_increment_ms
                time.sleep(sleep_increment_ms)
                
    @staticmethod
    def str_random(size:int):
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=size))

    def enqueue(self, dict_json:dict) -> None:
        name_file = JsonqueueFile.str_random(16)
        path_file_json = self.path_dir.joinpath(name_file)
        with path_file_json.open('w', encoding='utf-8') as file:
             json.dump(dict_json, file)


    def to_dict(self):
        dict_bytessource = {}
        dict_bytessource['type_jsonqueue'] = 'JsonqueueFile'
        dict_bytessource['path_dir'] = str(self.path_dir.absolute())
        return dict_bytessource

    @staticmethod
    def from_dict(dict_bytessource):
        if not dict_bytessource['type_jsonqueue'] == 'JsonqueueFile':
            raise Exception('incorrect_dict_type')
        return JsonqueueFile(Path(dict_bytessource['path_dir']))