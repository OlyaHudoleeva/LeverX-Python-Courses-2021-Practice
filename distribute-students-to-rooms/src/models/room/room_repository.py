import json
from abc import ABC, abstractmethod

from dicttoxml import dicttoxml


class RoomsRepositoryInterface(ABC):

    @abstractmethod
    def list_rooms(self):
        print('RoomsRepositoryInterface.list_rooms is called')

    @abstractmethod
    def save_rooms(self, new_filename, rooms):
        print('RoomsRepositoryInterface.save_rooms is called')


class RoomsFileRepositoryInterface(RoomsRepositoryInterface):

    def __init__(self, dir, filename):
        self.dir = dir
        self.filename = filename

    def list_rooms(self):
        print('RoomsFileRepositoryInterface.list_rooms is called')

    def save_rooms(self, new_filename, rooms):
        print('RoomsFileRepositoryInterface.save_rooms is called')


class RoomsJsonFileRepository(RoomsFileRepositoryInterface):

    def list_rooms(self):
        print('RoomsJsonFileRepository.list_rooms is called')

        with open(self.dir + '/' + self.filename, mode='r') as file:
            file_data = json.load(file)
            rooms = {room['id']: room for room in file_data}
            return rooms

    def save_rooms(self, new_filename, rooms):
        with open(self.dir + '/' + new_filename, 'w') as new_json_file:
            json.dump(list(rooms.values()), new_json_file)


class RoomsXmlFileRepository(RoomsFileRepositoryInterface):

    def list_rooms(self):
        print('RoomsXmlFileRepository.list_rooms is called')

    def save_rooms(self, new_filename, rooms):
        with open(self.dir + '/' + new_filename, "w") as new_xml_file:
            xml = dicttoxml(list(rooms.values()), item_func=lambda item: 'student').decode()
            new_xml_file.write(xml)
