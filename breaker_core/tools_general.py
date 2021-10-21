import sys
import os
import json
import string
import random
import zipfile

import pickle as pkl
import base64
import hashlib

from threading import Thread
from queue import Queue
from urllib.parse import urlparse

class ReporterProgress(object):

    def __init__(self, count_total):
        super(ReporterProgress, self).__init__()
        self.count_total = count_total
        self.count_progress = 0

    def report(self, progress=1):
        self.count_progress += progress
        percentage = round((self.count_progress/ self.count_total) * 100, 2)
        print('The percentage completed is ' + str(percentage))
        sys.stdout.flush()

class ManagedThread(object):
    """docstring for ManagedThread."""

    def __init__(self, queue_task, *, queue_error=None, reporter_progress=None):
        super(ManagedThread, self).__init__()

        self.queue_task = queue_task
        self.queue_error = queue_error
        self.reporter_progress = reporter_progress
        self.thread = Thread(target=self.run, daemon=True) 
        self.thread.start()

    def run(self):
        while True:
            try:
                runnable = self.queue_task.get(block=False)
                try:
                    runnable.run()
                    if self.reporter_progress:
                        self.reporter_progress.report()
                except Exception as error:
                    if self.reporter_progress:
                        self.reporter_progress.report()

                    if self.queue_error:
                        self.queue_error.put(error)
                    else:
                        print(error)
                        sys.stdout.flush()
            except Exception:
                break

    def join(self):
        self.thread.join()

class ToolsGeneral(object):    
   
    @staticmethod
    def complete_list_runnable(list_runnable, count_thread=10, report_progress=False):

        queue_runnable = Queue()
        reporter_progress = None
        if report_progress:
            reporter_progress = ReporterProgress(len(list_runnable))

        for runnable in list_runnable:
            queue_runnable.put(runnable)
        
        list_thread = []
        for _ in range(count_thread):
            list_thread.append(ManagedThread(queue_runnable, reporter_progress=reporter_progress))

        for thread in list_thread:
            thread.join()

    @staticmethod
    def md5_for_file(path_file):
        hash_md5 = hashlib.md5()
        with open(path_file, "rb") as file:
            for chunk in iter(lambda: file.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()

    @staticmethod
    def array_to_stringbase64(array):
        return base64.b64encode(pkl.dumps(array)).decode('utf-8')

    @staticmethod
    def stringbase64_to_array(stringbase64_array):
        return pkl.loads(base64.b64decode(stringbase64_array), encoding='utf-8')

    @staticmethod
    def random_string(length):
        return ''.join(random.choice(string.ascii_letters) for i in range(length))
        
    @staticmethod
    def create_id(prefix):
        return prefix + '-' + ToolsGeneral.random_string(16)

    # @staticmethod
    # def zip_dir(path_file_zip, path_file_source):
    #     with zipfile.ZipFile(path_file_zip, "w") as zip_reference:
    #         for name_file in os.listdir(path_dir_function):
    #             path_file_source = os.path.join(path_dir_function, name_file)
    #             zip_reference.write(path_file_source, name_file)


    @staticmethod
    def unzip_dir(path_file_zip, path_dir_target):
        with zipfile.ZipFile(path_file_zip, 'r') as zip_reference:
            zip_reference.extractall(path_dir_target)
  

  
    @staticmethod
    def index_bin(list_bin_limit, value):
        for index, bin_limit in enumerate(list_bin_limit):
            if value < bin_limit:
                return index
        return len(list_bin_limit)



    @staticmethod
    def url_get_extension(url):
       return urlparse(url).path.split('.')[-1]
        
# o = urlparse('http://www.cwi.nl:80/%7Eguido/Python.html')
# o   
# ParseResult(scheme='http', netloc='www.cwi.nl:80', path='/%7Eguido/Python.html',
#             params='', query='', fragment='')
    
    @staticmethod
    def str_is_int(str_value:str):
        try:
            int(str_value)
            return True
        except ValueError:
            return False

    
    @staticmethod
    def sha256_dict_json(dict_json:dict) -> 'str':
        return hashlib.sha256(json.dumps(dict_json).encode('utf-8')).hexdigest()