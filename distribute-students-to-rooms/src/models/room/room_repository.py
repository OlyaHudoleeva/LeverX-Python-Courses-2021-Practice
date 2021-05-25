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


class RoomsDbRepository(RoomsRepositoryInterface):

    def __init__(self, connection, table_name):
        self.connection = connection
        self.table_name = table_name

    def list_rooms(self):
        pass

    def clear_table(self):
        self.connection.cursor.execute('DELETE FROM {}'.format(self.table_name))

    def save_rooms(self, rooms):
        for room in rooms:
            self.connection.cursor.execute('INSERT INTO {} (id, name) VALUES (%s, %s)'.format(self.table_name),
                                           (room['id'], room['name']))

        self.connection.cnx.commit()


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
            return file_data

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
