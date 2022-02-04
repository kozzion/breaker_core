import os
import json
import time
import random
import string

from pathlib import Path
from typing import List

from breaker_core.datasource.jsonqueue import Jsonqueue

class JsonqueueDirect(Jsonqueue):

    def __init__(self, config:dict, service) -> None:
        super().__init__(config)
        self.service = service

    def exists(self) -> bool:
        return True
                
    def enqueue(self, dict_json:dict) -> None:
        self.service.process_request(dict_json)

    def to_dict(self):
        dict_bytessource = {}
        dict_bytessource['type_jsonqueue'] = 'JsonqueueDirect'
        return dict_bytessource
