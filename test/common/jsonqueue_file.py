import os
import json
import time

from pathlib import Path
from breaker_core.common.jsonqueue_file import JsonqueueFile

path_dir_test = Path('./test')
queue = JsonqueueFile(path_dir_test)
result = queue.dequeue()
print(result)
queue.enqueue({'test':'test'})
result = queue.dequeue()
print(result)
os.removedirs(path_dir_test)