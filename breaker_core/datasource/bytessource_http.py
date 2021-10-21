import os
import base64
import requests
from pathlib import Path

from breaker_core.datasource.bytessource import Bytessource

class BytessourceHttp(Bytessource):

    def __init__(self, url:str) -> None:
        self.url = url

    def exists(self) -> bool:
        return True

    def write(self, bytearray_object:bytearray) -> None:
        raise RuntimeError('bytessource is static readonly')

    def read(self) -> bytearray:
        return bytearray(base64.b64decode(self.str_base64))

    def delete(self) -> None:
        raise RuntimeError('bytessource is static readonly')
            
    def join(self, list_key:list[str]) -> Bytessource:
        raise RuntimeError('bytessource is static readonly')

    def list_shallow(self, prefix='') -> list[list[str]]:
        raise RuntimeError('bytessource is static readonly')

    def list_deep(self, prefix='') -> list[list[str]]:
        raise RuntimeError('bytessource is static readonly')

    def list_for_prefix(self, list_key_prefix:list[str]) -> list[list[str]]:
        raise RuntimeError('bytessource is static readonly')

    def to_dict(self) -> 'dict':
        dict_bytessource = {}
        dict_bytessource['type_bytessource'] = 'BytessourceHttp'
        dict_bytessource['url'] = self.url
        return dict_bytessource

    @staticmethod
    def from_dict(dict_bytessource) -> 'Bytessource':
        if not dict_bytessource['type_bytessource'] == 'BytessourceHttp':
            raise Exception('incorrect_dict_type')
        return BytessourceHttp(dict_bytessource['url'])

