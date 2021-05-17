import json
from abc import ABC, abstractmethod


class StudentsRepositoryInterface(ABC):

    @abstractmethod
    def list_students(self):
        print('StudentsRepositoryInterface.list_students is called')


class StudentsFileRepositoryInterface(StudentsRepositoryInterface):

    def __init__(self, dir, filename):
        self.dir = dir
        self.filename = filename

    def list_students(self):
        print('StudentsFileRepositoryInterface.list_students is called')


class StudentsJsonFileRepository(StudentsFileRepositoryInterface):

    def list_students(self):
        print('StudentsJsonFileRepository.list_students is called')

        with open(self.dir + '/' + self.filename, mode='r') as file:
            students = list(json.load(file))
            return [{"id": student['id'], "name": student['name'], "room": student['room']} for student in students]
