class StudentsToRoomsDistributor:

    def __init__(self, rooms, students):
        self.rooms = rooms
        self.students = students

    def __add_student_to_room(self, room, student):
        student_without_room = {"id": student['id'], "name": student['name']}
        if "students" not in room:
            room["students"] = [student_without_room]
        else:
            room["students"].append(student_without_room)

    def destribute(self):
        for student in self.students:
            for room in self.rooms:
                if student["room"] == room["id"]:
                    self.__add_student_to_room(room, student)
                    break

        # for room in self.rooms:
        #     room["students"] = list(filter(lambda student: student["room"] == room["id"], self.students))

        return self.rooms