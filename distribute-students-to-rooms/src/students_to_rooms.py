def __add_student_to_room(room, student):
    student_without_room = {"id": student['id'], "name": student['name']}
    if "students" not in room:
        room["students"] = [student_without_room]
    else:
        room["students"].append(student_without_room)


def destribute(rooms, students):
    for student in students:
        for room in rooms:
            if student["room"] == room["id"]:
                __add_student_to_room(room, student)
                break
    return rooms
