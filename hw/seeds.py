import sqlite3
import faker
from datetime import datetime
from random import randint, choice

NUMBER_GROUPS = 3
NUMBER_STUDENTS = 30
NUMBER_TEACHERS = 3
NUMBER_SUBJECTS = 5
NUMBER_MARKS = 20


def generate_fake_data(number_students, number_teachers) -> tuple:
    fake_groups = ['A', 'B', 'C']
    fake_subjects = ['Python', 'Java', 'JavaScript', 'C++', 'Go']
    fake_marks = [1, 2, 3, 4, 5]
    fake_students = []
    fake_teachers = []

    fake_data = faker.Faker('en-US')

    for _ in range(number_students):
        fake_students.append(fake_data.name())

    for _ in range(number_teachers):
        fake_teachers.append(fake_data.name())

    return fake_students, fake_teachers, fake_groups, fake_marks, fake_subjects


def prepare_data(students, teachers, groups, marks, subjects) -> tuple:
    for_groups = []
    for_teachers = []
    for_subjects = []
    for_students = []
    for_marks = []

    for group in groups:
        for_groups.append((group,))
    for teacher in teachers:
        for_teachers.append((teacher,))
    for subject in subjects:
        for_subjects.append((subject, randint(1, NUMBER_TEACHERS)))
    for student in students:
        for_students.append((student, randint(1, NUMBER_GROUPS)))
    for month in range(1, 11 + 1):
        mark_date = datetime(2021, month, randint(1, 30)).date()
        for student_id in range(1, NUMBER_STUDENTS + 1):
            for i in range(1, 2 + 1):
                for_marks.append((student_id, randint(1, NUMBER_SUBJECTS), choice(marks), mark_date))

    return for_students, for_teachers, for_groups, for_marks, for_subjects


def insert_data_to_db(students, teachers, groups, marks, subjects) -> None:
    with sqlite3.connect('db_students.db') as con:
        cur = con.cursor()

        sql_to_groups = """INSERT INTO groups(group_name)
                               VALUES (?)"""

        cur.executemany(sql_to_groups, groups)

        sql_to_teachers = """INSERT INTO teachers(name)
                                VALUES (?)"""
        cur.executemany(sql_to_teachers, teachers)

        sql_to_students = """INSERT INTO students(name, group_id)
                                VALUES(?,?)"""
        cur.executemany(sql_to_students, students)

        sql_to_subjects = """INSERT INTO subjects(name, teacher_id)
                                VALUES(?,?)"""
        cur.executemany(sql_to_subjects, subjects)

        sql_to_marks = """INSERT INTO marks(student_id, subject_id, mark, created_at)
                                VALUES(?,?,?,?)"""
        cur.executemany(sql_to_marks, marks)
        con.commit()


if __name__ == '__main__':
    students, teachers, groups, marks, subjects = generate_fake_data(NUMBER_STUDENTS, NUMBER_TEACHERS)
    students, teachers, groups, marks, subjects = prepare_data(students, teachers, groups, marks, subjects)
    insert_data_to_db(students, teachers, groups, marks, subjects)
