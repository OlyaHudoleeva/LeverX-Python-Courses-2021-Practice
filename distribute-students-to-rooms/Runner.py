from src import students_to_rooms
from src.models.room import room_repository
from src.models.student import student_repository
from src.parser import parser
from src.util import util

parser = parser.createParser()
namespace = parser.parse_args()

rooms_dir, rooms_filename = util.split_path(namespace.rooms)
students_dir, students_filename = util.split_path(namespace.students)

room_reader: room_repository.RoomsRepositoryInterface = room_repository.RoomsJsonFileRepository(
    rooms_dir, rooms_filename)
rooms = room_reader.listRooms()

student_reader: student_repository.StudentsRepositoryInterface = student_repository.StudentsJsonFileRepository(
    students_dir, students_filename)
students = student_reader.listStudents()

distributor = students_to_rooms.StudentsToRoomsDistributor(rooms, students)

rooms_with_students = distributor.destribute()

if namespace.format == "json":
    room_reader.saveRooms("rooms_with_students.json", rooms_with_students)
elif namespace.format == "xml":
    xml_room_reader = room_repository.RoomsXmlFileRepository("resources", "rooms.xml")
    xml_room_reader.saveRooms("rooms_with_students.xml", rooms_with_students)
