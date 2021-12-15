import os
import json

from pathlib import Path

from breaker_core.datasource.bytessource_file import BytessourceFile

path_file_config_breaker = Path(os.getenv('PATH_FILE_CONFIG_BREAKER_AWS_DEV', '/config/config.cfg'))
with open(path_file_config_breaker, 'r') as file:
    config_breaker = json.load(file)

path_dir_test = Path('./test')
generator = BytessourceFile(config_breaker ,path_dir_test)
bytearray_source = generator.join(['result.wav'])
print(bytearray_source.exists())
bytearray_source.write(bytearray('test'.encode('utf-8')))
print(bytearray_source.exists())
bytearray = bytearray_source.read()
print(bytearray)
bytearray_source.delete()
print(bytearray_source.exists())