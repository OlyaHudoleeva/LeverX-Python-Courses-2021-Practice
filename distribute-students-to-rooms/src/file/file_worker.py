import json
from abc import ABC, abstractmethod

from dicttoxml import dicttoxml


class FileWorkerInterface(ABC):

    def __init__(self, dir, filename):
        self.dir = dir
        self.filename = filename

    @abstractmethod
    def read_data(self):
        pass

    @abstractmethod
    def write_data(self):
        pass


class JsonFileWorker(FileWorkerInterface):

    def read_data(self):
        with open(self.dir + '/' + self.filename, mode='r') as file:
            file_data = json.load(file)
            return file_data

    def write_data(self, ls):
        with open(self.dir + '/' + self.filename, 'w') as new_json_file:
            json.dump(ls, new_json_file)


class XmlFileWorker(FileWorkerInterface):

    def read_data(self):
        pass

    def write_data(self, ls, func=lambda item: 'list_item'):
        with open(self.dir + '/' + self.filename, "w") as new_xml_file:
            xml = dicttoxml(ls, item_func=func).decode()
            new_xml_file.write(xml)
