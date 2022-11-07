import sqlite3
import os.path


def create_db():
    with open('students.sql', 'r') as file:
        sql = file.read()

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, "db_students.db")

    with sqlite3.connect(db_path) as con:
        cur = con.cursor()
        cur.executescript(sql)


if __name__ == "__main__":
    create_db()
