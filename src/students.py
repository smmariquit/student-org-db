import mariadb

def print_student_header():
    print("""┌────────────────────────────────────────────────────────────
│                 👥 Student Management                     """)

def print_student_menu():
    print("""📋 Student Menu:
┌────────────────────────────────────────────────────────────
│ [1] ➕ Add Student                                        
│ [2] ✏️  Update Student                                     
│ [3] 🗑️  Delete Student                                     
│ [4] 👀 View Students                                      
│ [0] ↩️  Back                                                
└────────────────────────────────────────────────────────────""")

def add_student(conn):
    print("""┌────────────────────────────────────────────────────────────
│                    ➕ Add New Student                     """)
    student_id = input("🎓 Enter Student ID: ")
    first_name = input("👤 Enter First Name: ")
    middle_name = input("👤 Enter Middle Name (press Enter if none): ")
    last_name = input("👤 Enter Last Name: ")
    gender = input("👥 Enter Gender: ")
    degree_program = input("📚 Enter Degree Program: ")
    
    try:
        cursor = conn.cursor()
        
        # Insert the new student into member table
        cursor.execute(
            """INSERT INTO member 
               (`Student Number`, `First Name`, `Middle Name`, `Last Name`, `Gender`, `Degree Program`) 
               VALUES (?, ?, ?, ?, ?, ?)""",
            (student_id, first_name, middle_name or None, last_name, gender, degree_program) # If middle name is empty, it will be Falsy. Since it's OR'd to None, it will only not be None if middle_name is not empty. https://www.freecodecamp.org/news/truthy-and-falsy-values-in-python/
        )
        conn.commit() # In mariadb-python, this saves data. This is different from MariaDB commits.
        
        print("\n📝 Student Information to be added:")
        print("┌────────────────────────────────────────────────────────────")
        print(f"│ 🎓 ID: {student_id}")
        print(f"│ 👤 Name: {first_name} {middle_name + ' ' if middle_name else ''}{last_name}") # If no middle name, it will not print anything.
        print(f"│ 👥 Gender: {gender}")
        print(f"│ 📚 Degree Program: {degree_program}")
        print("└────────────────────────────────────────────────────────────")
        print("\n✅ Student successfully added to database!")
        
    except mariadb.Error as e:
        print(f"\n❌ Error adding student: {e}")

def update_student(conn):
    print("""┌────────────────────────────────────────────────────────────
│                     ✏️  Update Student                     """)
    student_id = input("🔍 Enter Student ID to update: ")
    
    try:
        cursor = conn.cursor()
        
        # Get current student info
        cursor.execute(
            "SELECT student_id, name FROM students WHERE student_id = ?",
            (student_id,)
        )
        student = cursor.fetchone() # Defensive programming. If somehow there are duplicate student IDs, it will only fetch the first one.
        
        if student:
            print("\n📋 Current Student Information:")
            print("┌────────────────────────────────────────────────────────────")
            print(f"│ 🎓 ID: {student[0]}")
            print(f"│ 👤 Name: {student[1]} {student[2] + ' ' if student[2] else ''}{student[3]}") # If no middle name, it will not print anything.
            print(f"│ 👥 Gender: {student[4]}")
            print(f"│ 📚 Degree Program: {student[5]}")
            print("└────────────────────────────────────────────────────────────")
            
            while True:
                print("\n📝 What would you like to update?")
                print("┌────────────────────────────────────────────────────────────")
                print("│ [1] 👤 Name                                                ")
                print("│ [0] ↩️  Back                                                ")
                print("└────────────────────────────────────────────────────────────")
                
                choice = input("Enter your choice: ")
                if choice == "0":
                    break
                elif choice == "1":
                    new_name = input("👤 Enter new Student Name: ")
                    cursor.execute(
                        "UPDATE students SET name = ? WHERE student_id = ?",
                        (new_name, student_id)
                    )
                    conn.commit()
                    print(f"✅ Student name updated to: {new_name}")
        else:
            print(f"\n❌ Student with ID {student_id} not found!")
            
    except mariadb.Error as e:
        print(f"\n❌ Error updating student: {e}")

def delete_student(conn):
    print("""┌────────────────────────────────────────────────────────────
│                     🗑️  Delete Student                     """)
    student_id = input("🔍 Enter Student ID to delete: ")
    
    try:
        cursor = conn.cursor()
        
        # Get student info before it gets deleted
        cursor.execute(
            "SELECT student_id, name FROM students WHERE student_id = ?",
            (student_id,)
        )
        student = cursor.fetchone()
        
        if student:
            print("\n⚠️  Student Information to be deleted:")
            print("┌────────────────────────────────────────────────────────────")
            print(f"│ 🎓 ID: {student[0]}")
            print(f"│ 👤 Name: {student[1]} {student[2] + ' ' if student[2] else ''}{student[3]}") # If no middle name, it will not print anything.
            print(f"│ 👥 Gender: {student[4]}")
            print(f"│ 📚 Degree Program: {student[5]}")
            print("└────────────────────────────────────────────────────────────")
            
            confirm = input("\n⚠️  Are you sure you want to delete this student? (Y/N): ").upper()
            if confirm == "Y":
                cursor.execute(
                    "DELETE FROM students WHERE student_id = ?",
                    (student_id,)
                )
                conn.commit()
                print("✅ Student successfully deleted from database!")
        else:
            print(f"\n❌ Student with ID {student_id} not found!")
            
    except mariadb.Error as e:
        print(f"\n❌ Error deleting student: {e}")

def view_students(conn):
    while True:
        print("""┌────────────────────────────────────────────────────────────
│                     👀 View Students                      """)
        print("📋 View Options:")
        print("┌────────────────────────────────────────────────────────────")
        print("│ [1] 📋 View All Students                                   ")
        print("│ [0] ↩️  Back                                                ")
        print("└────────────────────────────────────────────────────────────")
        
        choice = input("Enter your choice: ")
        if choice == "0":
            break
        elif choice == "1":
            try:
                cursor = conn.cursor()
                
                # Use the query from queries.py
                query = """
                    SELECT 
                        `Student Number`,
                        `First Name`,
                        `Middle Name`,
                        `Last Name`,
                        `Gender`,
                        `Degree Program`
                    FROM member
                    ORDER BY `Student Number`
                """
                cursor.execute(query)
                students = cursor.fetchall()
                
                if students:
                    print("\n📋 Student List:")
                    for student in students:
                        student_id = student[0]
                        first_name = student[1]
                        middle_name = student[2] if student[2] else ""
                        last_name = student[3]
                        gender = student[4]
                        degree = student[5]
                        
                        # Format the name with middle name if present
                        full_name = f"{first_name} {middle_name + ' ' if middle_name else ''}{last_name}"
                        
                        print("┌────────────────────────────────────────────────────────────")
                        print(f"│ 🎓 ID: {student_id}")
                        print(f"│ 👤 Name: {full_name}")
                        print(f"│ 👥 Gender: {gender}")
                        print(f"│ 📚 Degree: {degree}")
                        print("└────────────────────────────────────────────────────────────")
                else:
                    print("\n📋 No students found in the database.")
                    
            except mariadb.Error as e:
                print(f"\n❌ Error viewing students: {e}")

def main(conn):
    while True:
        print_student_header()
        print_student_menu()
        choice = input("Enter your choice: ")
        
        if choice == "0":
            break
        elif choice == "1":
            add_student(conn)
        elif choice == "2":
            update_student(conn)
        elif choice == "3":
            delete_student(conn)
        elif choice == "4":
            view_students(conn)

if __name__ == "__main__": # Best practice for OOP in Python. When you import this file, it will not run automatically because __name__ will be the name of the file.
                            # However, when you run this file directly via python main.py, __name__ will be "__main__" and the code below will run.
    main()
