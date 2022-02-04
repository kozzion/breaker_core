import os
import sys
from pathlib import Path
from typing import List
from breaker_core.datasource.bytessource import Bytessource

class BytessourcePrint(Bytessource):

    def __init__(self, config:dict, charset:str='utf-8') -> None:
        super().__init__(config)
        self.charset = charset

    def write(self, bytes:bytes) -> None:
        print(bytes.decode(self.charset))
        sys.stdout.flush()

    def to_dict(self) -> 'dict':
        dict_bytessource = {}
        dict_bytessource['type_bytessource'] = 'BytessourcePrint'
        dict_bytessource['charset'] = self.charset
        return dict_bytessource

    @staticmethod
    def from_dict(config:dict, dict_bytessource) -> 'Bytessource':
        if not dict_bytessource['type_bytessource'] == 'BytessourcePrint':
            raise Exception('incorrect_dict_type')

        return BytessourcePrint(config, 
            dict_bytessource['charset'])

