from src import rooms_with_students_service
from src.db_init.db_initializer import DbConnector, DbCreator
from src.file.file_worker import JsonFileWorker, XmlFileWorker
from src.models.room.room_repository import RoomsRepositoryInterface, RoomsJsonFileRepository, RoomsDbRepository
from src.models.student.student_repository import StudentsRepositoryInterface, StudentsJsonFileRepository, \
    StudentsDBRepository
from src.parser import parser
from src.util import util

DB_NAME = 'task4_db_v2'

TABLES = {
    'rooms': ('CREATE TABLE IF NOT EXISTS rooms (id int(5) PRIMARY KEY, name varchar(20))'),
    'students': ('CREATE TABLE IF NOT EXISTS students (id int(5) PRIMARY KEY, name varchar(30), birthday datetime(6), '
                 'room int(5), sex enum(\'M\',\'F\'), FOREIGN KEY (room) REFERENCES rooms (id))')
}

QUERIES = {
    'students_in_rooms': 'SELECT rooms.id, rooms.name, COUNT(students.id) AS students_in_room FROM rooms LEFT JOIN students ON rooms.id = students.room GROUP BY rooms.id, rooms.name',
    'rooms_with_smallest_average_age': 'SELECT rooms.id, rooms.name, AVG(date_format(from_days(datediff(current_date(), students.birthday)), "%Y")+0) AS av_age FROM rooms LEFT JOIN students ON rooms.id = students.room group by rooms.id, rooms.name having av_age is not null order by av_age asc LIMIT 5',
    'rooms_with_biggest_age_diff': 'SELECT rooms.id, rooms.name, max(date_format(from_days(datediff(current_date(), students.birthday)), "%Y")+0)-min(date_format(from_days(datediff(current_date(), students.birthday)), "%Y")+0) AS age_diff FROM rooms LEFT JOIN students ON rooms.id = students.room group by rooms.id, rooms.name order by age_diff desc LIMIT 5',
    'rooms_with_different_sexes_students': 'select distinct rooms.id from rooms join students on rooms.id = students.room where students.sex = \'F\' and rooms.id in (select rooms.id from rooms join students on rooms.id = students.room where students.sex = \'M\') order by rooms.id asc',
}


def main():
    con = DbConnector()
    db_creator = DbCreator(con)
    db_creator.create_database(DB_NAME)
    db_creator.use_database(DB_NAME)
    db_creator.create_tables(TABLES)

    arg_parser = parser.create_parser()
    namespace = arg_parser.parse_args()

    students_dir, students_filename = util.split_path(namespace.students)
    rooms_dir, rooms_filename = util.split_path(namespace.rooms)

    room_reader: RoomsRepositoryInterface = RoomsJsonFileRepository(
        rooms_dir, rooms_filename)
    rooms = room_reader.list_rooms()

    rooms_for_db = RoomsDbRepository(con, list(TABLES.keys())[0])

    student_reader: StudentsRepositoryInterface = StudentsJsonFileRepository(
        students_dir, students_filename)
    students = student_reader.list_students()

    students_for_db = StudentsDBRepository(con, list(TABLES.keys())[1])

    students_for_db.clear_table()
    rooms_for_db.clear_table()
    rooms_for_db.save_rooms(rooms)
    students_for_db.save_students(students)

    rooms_with_students = rooms_with_students_service.execute_query(con, QUERIES)
    print(rooms_with_students)

    if namespace.format == "json":
        for filename, result in rooms_with_students.items():
            json_worker = JsonFileWorker("resources", filename + '.json')
            json_worker.write_data(result)
    elif namespace.format == "xml":
        for filename, result in rooms_with_students.items():
            xml_worker = XmlFileWorker("resources", filename + '.xml')
            xml_worker.write_data(result)

    con.close()


if __name__ == "__main__":
    main()
