from ..utils import prepare_objects

user_keys = ["name", "email", "password", "in_batches", "faculty_events"]
student_ukeys = ["uid", "semester", "division", "passout"]
faculty_ukeys = ["code", "default_room"]

student_keys = user_keys + student_ukeys
faculty_keys = user_keys + faculty_ukeys

students = [
    ["Rishi Tiku", "rishi.tiku@spit.ac.in", "12345678", [], [], "2021700067", 7, "D", 2025],
    ["Arsh Raina", "arsh.raina@spit.ac.in", "12345678", [], [], "2021600054", 7, "C", 2025],
]

faculties = [
    ["Aparna Halbe", "aparna_halbe@spit.ac.in", "12345678", [], [], "AH", None],
    ["Dayanand Ambavade", "dd_ambavade@spit.ac.in", "12345678", [], [], "DDA", None], 
    ["Pramod Bide", "pramod_bide@spit.ac.in", "12345678", [], [], "PB", None],
]

def get_student_objects():
    return prepare_objects(student_keys, students)

def get_faculty_objects():
    return prepare_objects(faculty_keys, faculties)


if __name__ == "__main__":
    print(*get_student_objects(), sep="\n")
    print(*get_faculty_objects(), sep="\n")

