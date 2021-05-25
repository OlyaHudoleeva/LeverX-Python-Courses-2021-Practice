import json
from abc import ABC, abstractmethod


class StudentsRepositoryInterface(ABC):

    @abstractmethod
    def list_students(self):
        print('StudentsRepositoryInterface.list_students is called')


class StudentsDBRepository(StudentsRepositoryInterface):

    def __init__(self, connection, table_name):
        self.connection = connection
        self.table_name = table_name

    def list_students(self):
        pass

    def clear_table(self):
        self.connection.cursor.execute('DELETE FROM {}'.format(self.table_name))

    def save_students(self, students):
        for student in students:
            self.connection.cursor.execute(
                'INSERT INTO {} (birthday, id, name, room, sex) VALUES (DATE_FORMAT(%s, "%Y-%m-%d %H:%i:%S.%f"), %s, %s, %s, %s)'.format(
                    self.table_name),
                (student['birthday'], student['id'], student['name'], student['room'], student['sex']))

            self.connection.cnx.commit()


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
            return students
