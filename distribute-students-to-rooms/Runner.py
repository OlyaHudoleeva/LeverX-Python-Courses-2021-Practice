from src import students_to_rooms
from src.models.room.room_repository import RoomsRepositoryInterface, RoomsJsonFileRepository, RoomsXmlFileRepository
from src.models.student.student_repository import StudentsRepositoryInterface, StudentsJsonFileRepository
from src.parser import parser
from src.util import util


def main():
    arg_parser = parser.create_parser()
    namespace = arg_parser.parse_args()

    rooms_dir, rooms_filename = util.split_path(namespace.rooms)
    students_dir, students_filename = util.split_path(namespace.students)

    room_reader: RoomsRepositoryInterface = RoomsJsonFileRepository(
        rooms_dir, rooms_filename)
    rooms = room_reader.list_rooms()

    student_reader: StudentsRepositoryInterface = StudentsJsonFileRepository(
        students_dir, students_filename)
    students = student_reader.list_students()

    rooms_with_students = students_to_rooms.destribute(rooms, students)

    if namespace.format == "json":
        room_reader.save_rooms("rooms_with_students.json", rooms_with_students)
    elif namespace.format == "xml":
        xml_room_reader = RoomsXmlFileRepository("resources", "rooms.xml")
        xml_room_reader.save_rooms("rooms_with_students.xml", rooms_with_students)


if __name__ == "__main__":
    main()
