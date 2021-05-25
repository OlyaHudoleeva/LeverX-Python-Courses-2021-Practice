def __add_student_to_room(room, student):
    student_without_room = {"id": student['id'], "name": student['name']}
    if "students" not in room:
        room["students"] = [student_without_room]
    else:
        room["students"].append(student_without_room)


def destribute(rooms, students):
    rooms = {room['id']: room for room in rooms}
    students = [{"id": student['id'], "name": student['name'], "room": student['room']} for student in students]
    for student in students:
        student_room = rooms[student["room"]]
        if student_room:
            __add_student_to_room(student_room, student)
    return rooms
