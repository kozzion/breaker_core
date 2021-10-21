import os
from pathlib import Path

from breaker_core.datasource.bytessource import Bytessource

class BytessourceBytearray(Bytessource):

    def __init__(self, bytearray:bytearray) -> None:
        self.bytearray = bytearray

    def exists(self) -> bool:
        return True

    def write(self, bytearray_object:bytes) -> None:
        raise RuntimeError('bytessource is static readonly')

    def read(self) -> bytearray:
        return self.bytearray

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
        raise RuntimeError('bytessource is not serialiazable')

    @staticmethod
    def from_dict(dict_bytessource) -> 'Bytessource':
        raise RuntimeError('bytessource is not serialiazable')


