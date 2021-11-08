import os
import base64
from pathlib import Path

from breaker_core.datasource.bytessource import Bytessource

class BytessourceBase64(Bytessource):

    def __init__(self, config:dict, str_base64) -> None:
        super().__init__(config)
        self.str_base64 = str_base64

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
        dict_bytessource['type_bytessource'] = 'BytessourceBase64'
        dict_bytessource['str_base64'] = self.str_base64
        return dict_bytessource

    @staticmethod
    def from_dict(config:dict, dict_bytessource) -> 'Bytessource':
        if not dict_bytessource['type_bytessource'] == 'BytessourceBase64':
            raise Exception('incorrect_dict_type')
        return BytessourceBase64(config, dict_bytessource['str_base64'])

