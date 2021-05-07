import json


class StudentsRepositoryInterface:

    def listStudents(self):
        print('StudentsRepositoryInterface.listStudents is called')


class StudentsFileRepositoryInterface(StudentsRepositoryInterface):

    def __init__(self, dir, filename):
        self.dir = dir
        self.filename = filename

    def listStudents(self):
        print('StudentsFileRepositoryInterface.listStudents is called')


class StudentsJsonFileRepository(StudentsFileRepositoryInterface):

    def listStudents(self):
        print('StudentsJsonFileRepository.listStudents is called')

        with open(self.dir + '/' + self.filename, mode='r') as file:
            students = list(json.load(file))
            return list(
                map(lambda student: {"id": student['id'], "name": student['name'], "room": student['room']}, students))
