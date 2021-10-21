from breaker_core.common.bytessource_generator_file import BytessourceGeneratorFile
from breaker_core.common.bytessource_file import BytessourceFile
from pathlib import Path

path_dir_test = Path('./test')
generator = BytessourceGeneratorFile(path_dir_test)
bytearray_source = generator.generate(['result.wav'])
print(bytearray_source.exists())
bytearray_source.save(bytearray('test'.encode('utf-8')))
print(bytearray_source.exists())
bytearray = bytearray_source.load()
print(bytearray)
bytearray_source.delete()
print(bytearray_source.exists())
# class BytessourceFile(BytessourceBase):

#     def __init__(self, path_file:Path) -> None:
#         self.path_file = path_file

#     def exists(self) -> bool:
#         return self.path_file.exists()

#     def save(self, bytearray_object:bytearray) -> None:
#         with open(self.path_file, 'wb') as file:
#             file.write(bytearray_object)

#     def load(self) -> bytearray:
#         with open(self.path_file, 'rb') as file:
#             return file.read()

#     def to_dict(self):
#         dict_bytessource = {}
#         dict_bytessource['type_bytessource'] = 'BytessourceFile'
#         dict_bytessource['path_file'] = str(self.path_file)
#         return dict_bytessource

#     @staticmethod
#     def from_dict(self, dict_bytessource):
#         if not dict_bytessource['type_bytessource'] == 'BytessourceFile':
#             raise Exception('incorrect_dict_type')
#         return BytessourceFile(dict_bytessource['path_file'])
