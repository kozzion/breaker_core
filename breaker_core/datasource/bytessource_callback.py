import os
import base64
import requests
from pathlib import Path
from typing import List
from typing import Dict

from breaker_core.datasource.bytessource import Bytessource

class BytessourceCallback(Bytessource):

    def __init__(self, config:Dict, url_callback) -> None:
        super().__init__(config)
        self.url_callback = url_callback

    def exists(self) -> bool:
        return True

    def write(self, bytearray_object:bytearray) -> None:
        raise RuntimeError('bytessource is static writeonly')

    def write_json(self, dict_json:Dict) -> None:
        requests.post(self.url_callback, json=dict_json)

    def read(self) -> bytearray:
        raise RuntimeError('bytessource is static writeonly')

    def delete(self) -> None:
        raise RuntimeError('bytessource is static writeonly')
            
    def join(self, list_key:List[str]) -> Bytessource:
        raise RuntimeError('bytessource is static writeonly')

    def list_shallow(self, prefix='') -> List[List[str]]:
        raise RuntimeError('bytessource is static writeonly')

    def list_deep(self, prefix='') -> List[List[str]]:
        raise RuntimeError('bytessource is static writeonly')

    def list_for_prefix(self, list_key_prefix:List[str]) -> List[List[str]]:
        raise RuntimeError('bytessource is static writeonly')

    def to_dict(self) -> 'dict':
        dict_bytessource = {}
        dict_bytessource['type_bytessource'] = 'BytessourceCallback'
        dict_bytessource['url_callback'] = self.url_callback
        return dict_bytessource

    @staticmethod
    def from_dict(config:dict, dict_bytessource) -> 'Bytessource':
        if not dict_bytessource['type_bytessource'] == 'BytessourceCallback':
            raise Exception('incorrect_dict_type')
        return BytessourceCallback(config, dict_bytessource['url_callback'])

