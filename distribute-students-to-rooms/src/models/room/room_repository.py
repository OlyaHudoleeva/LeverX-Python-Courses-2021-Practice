import json

from dicttoxml import dicttoxml


class RoomsRepositoryInterface:

    def listRooms(self):
        print('RoomsRepositoryInterface.listRooms is called')

    def saveRooms(self, new_filename, rooms):
        pass


class RoomsFileRepositoryInterface(RoomsRepositoryInterface):

    def __init__(self, dir, filename):
        self.dir = dir
        self.filename = filename

    def listRooms(self):
        print('RoomsFileRepositoryInterface.listRooms is called')

    def saveRooms(self, new_filename, rooms):
        pass


class RoomsJsonFileRepository(RoomsFileRepositoryInterface):

    def listRooms(self):
        print('RoomsJsonFileRepository.listRooms is called')

        with open(self.dir + '/' + self.filename, mode='r') as file:
            rooms = list(json.load(file))
            return list(map(lambda room: {"id": room['id'], "name": room['name']}, rooms))

    def saveRooms(self, new_filename, rooms):
        with open(self.dir + '/' + new_filename, 'w') as new_json_file:
            json.dump(rooms, new_json_file)


class RoomsXmlFileRepository(RoomsFileRepositoryInterface):

    def listRooms(self):
        print('RoomsXmlFileRepository.listRooms is called')

    def saveRooms(self, new_filename, rooms):
        with open(self.dir + '/' + new_filename, "w") as new_xml_file:
            xml = dicttoxml(rooms, item_func=lambda item: 'student').decode()
            new_xml_file.write(xml)
