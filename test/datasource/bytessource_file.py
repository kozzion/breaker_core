from breaker_core.datasource.bytessource_file import BytessourceFile
from pathlib import Path

path_dir_test = Path('./test')
generator = BytessourceFile(path_dir_test)
bytearray_source = generator.generate(['result.wav'])
print(bytearray_source.exists())
bytearray_source.save(bytearray('test'.encode('utf-8')))
print(bytearray_source.exists())
bytearray = bytearray_source.load()
print(bytearray)
bytearray_source.delete()
print(bytearray_source.exists())