def create_student(cursor, student_number, first_name, middle_name, last_name, gender, degree_program):
    query = """
        INSERT INTO member (`Student Number`, `First Name`, `Middle Name`, `Last Name`, `Gender`, `Degree Program`)
        VALUES (?, ?, ?, ?, ?, ?)
    """
    cursor.execute(query, (student_number, first_name, middle_name, last_name, gender, degree_program))

def get_student_by_id(cursor, student_number):
    query = "SELECT * FROM member WHERE `Student Number` = ?"
    cursor.execute(query, (student_number,))
    return cursor.fetchone()