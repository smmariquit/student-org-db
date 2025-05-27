import mariadb

student_id = None

# transferred this to main
# def student_auth(conn):
#     print("""┌────────────────────────────────────────────────────────────
# │                 👥 Student Management                     """)
    
#     student_id = input("🎓 Enter Student ID: ")
    
#     try:
#         cursor = conn.cursor()
        
#         cursor.execute("SELECT * FROM member WHERE `Student Number` = ?", (student_id,))
#         student = cursor.fetchone()
#         if student:
#             return student[0]
#         else:
#             print(f"\n❌ Student with ID {student_id} not found!")
#             return None
#     except mariadb.Error as e:
#         print(f"\n❌ Error authenticating student: {e}")
        

def print_student_header():
    print("""┌────────────────────────────────────────────────────────────
│                 👥 Student Management                     """)

def print_student_menu():
    print("""📋 Student Menu:
┌────────────────────────────────────────────────────────────
│ [1] View Organizations
│ [2] View Committees
│ [3] View Fees
│ [0] ↩️  Back                                                
└────────────────────────────────────────────────────────────""")

def view_organizations(conn, student_id):
    print("""┌────────────────────────────────────────────────────────────
│                    ➕ View Organizations                     """)
         
    try:
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM organization JOIN joins ON organization.`Organization ID` = joins.`Organization ID` JOIN member ON member.`Student Number` = joins.`Student Number` WHERE member.`Student Number` = ?", (student_id,))
        organizations = cursor.fetchall()
    except mariadb.Error as e:
        print(f"\n❌ Error viewing organizations: {e}")

    if organizations:
        print("\n📋 Organizations:")
        for organization in organizations:
            print(f"│ 🔢 ID: {organization[0]}")
            print(f"│ 🏢 Name: {organization[1]}")
            print("└────────────────────────────────────────────────────────────")
    else:
        print("\n📋 No organizations found.")

def view_committees(conn, student_id):
    print("""┌────────────────────────────────────────────────────────────
│                    👥 View Committees                     """)
    try:
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT DISTINCT c.`Committee Name`, c.`Organization ID`, o.`Organization Name`, sr.`Role`
            FROM student_role sr
            JOIN committee c ON sr.`Committee Name` = c.`Committee Name` 
                AND sr.`Organization ID` = c.`Organization ID`
            JOIN organization o ON c.`Organization ID` = o.`Organization ID`
            WHERE sr.`Student Number` = ?
            ORDER BY c.`Committee Name`
        """, (student_id,))
        committees = cursor.fetchall()
    except mariadb.Error as e:
        print(f"\n❌ Error viewing committees: {e}")

    if committees:
        print("\n📋 Your Committees:")
        for committee in committees:
            print("┌────────────────────────────────────────────────────────────")
            print(f"│ 🏢 Committee: {committee[0]}")
            print(f"│ 🏛️ Organization: {committee[2]}")
            print(f"│ 👤 Your Role: {committee[3]}")
            print("└────────────────────────────────────────────────────────────")
    else:
        print("\n📋 You are not a member of any committees.")

def view_fees(conn, student_id):
    while True:
        print("""┌────────────────────────────────────────────────────────────
    │                    💰 View Fees                     """)
        print("""📋 View Fees Menu:
        ┌────────────────────────────────────────────────────────────
        │ [1] View Unpaid Dues Across All Orgs
        │ [2] View Fees Past Due
        │ [3] View All Fees
        │ [0] ↩️  Back                                                
        └────────────────────────────────────────────────────────────""")
        choice = input("Enter your choice: ")
        if choice == "0":
            break
        elif choice == "1":
            try:
                cursor = conn.cursor()
                cursor.execute(
                    """CREATE OR REPLACE VIEW unpaid_fees_membervu(student_number, organization_id, fee_name, amount, due_date, academic_year, semester)
                            AS SELECT f.`Student Number`, f.`Organization ID`, f.`Fee Name`, f.`Amount`, f.`Due Date`, f.`Academic Year`, f.`Semester`
                            FROM fee f
                            WHERE f.`Status` = 'Unpaid' OR f.`Status` = 'Pending'
                            AND f.`Student Number` = ?""",
                            (student_id,))

                cursor.execute(
                """SELECT * FROM unpaid_fees_membervu
                    WHERE student_number = ?"""
                , (student_id,))
                results = cursor.fetchall() 

                # working, wonky lang display
                if results:
                    print("\n📋 Unpaid Dues Across All Organizations")
                    print("┌────────────┬──────────────┬─────────────────────┬──────────┬────────────┬───────────────┬───────────┐")
                    print("│ Student #  │ Org ID       │ Fee Name            │ Amount   │ Due Date   │ Academic Year │ Semester  │")
                    print("├────────────┼──────────────┼─────────────────────┼──────────┼────────────┼───────────────┼───────────┤")

                    for row in results:
                        print(f"│ {row[0]:<11} │ {row[1]:<12} │ {row[2]:<19} │ ₱{row[3]:<7} │ {str(row[4]):<10} │ {row[5]:<13} │ {row[6]:<9} │")

                    print("└────────────┴──────────────┴─────────────────────┴──────────┴────────────┴───────────────┴───────────┘\n")
                else:
                    print("\nℹ️  No unpaid dues found for this member.\n")

            except mariadb.Error as e:
                print(f"\n❌ Error fetching report: {e}")

        elif choice == "2":
            try:
                cursor = conn.cursor()
                cursor.execute(
                    """SELECT * FROM fee WHERE `Student Number` = ?
                    AND `Status` != 'Paid'
                    AND `Due Date` < CURDATE()""",
                    (student_id,)
                )
                results = cursor.fetchall()

                if results:
                    print("\n📋 Fees Past Due Across All Organizations")
                    print("┌──────────────────┬────────────────┬──────────────────────┬────────────┬────────────────┬────────────┬──────────┐")
                    print("│ Organization ID  │ Student Number │ Fee Name             │ Due Date   │ Academic Year  │ Semester   │ Amount   │")
                    print("├──────────────────┼────────────────┼──────────────────────┼────────────┼────────────────┼────────────┼──────────┤")

                    for row in results:
                        print(f"│ {row[0]:<16} │ {row[1]:<14} │ {row[2]:<20} │ {row[3]:<10} │ {row[4]:<14} │ {row[6]:<10} │ ₱{row[7]:<7} │")

                    print("└──────────────────┴────────────────┴──────────────────────┴────────────┴────────────────┴────────────┴──────────┘\n")
                else:
                    print("\nℹ️  No unpaid feed past their due date found for this member.\n")

            except mariadb.Error as e:
                print(f"\n❌ Error fetching report: {e}")
                    
        elif choice == "3":
            try:
                cursor = conn.cursor()
                
                cursor.execute("""
                    SELECT f.*, o.`Organization Name` 
                    FROM fee f 
                    JOIN organization o ON f.`Organization ID` = o.`Organization ID`
                    WHERE f.`Student Number` = ?
                    ORDER BY f.`Due Date` DESC
                """, (student_id,))
                fees = cursor.fetchall()
            except mariadb.Error as e:
                print(f"\n❌ Error viewing fees: {e}")
            
            if fees:
                print("\n📋 Fees:")
                for fee in fees:
                    print("┌────────────────────────────────────────────────────────────")
                    print(f"│ 🏢 Organization: {fee[8]}")
                    print(f"│ 💰 Fee Name: {fee[2]}")
                    print(f"│ 📅 Due Date: {fee[3]}")
                    print(f"│ 📚 Academic Year: {fee[4]}")
                    print(f"│ 🔃 Status: {fee[5]}")
                    print(f"│ 🗓️ Semester: {fee[6]}")
                    print(f"│ 💳 Amount: ₱{float(fee[7]):.2f}")
                    print("└────────────────────────────────────────────────────────────")
            else:
                print("\n📋 No fees found.")

# def add_student(conn):
#     print("""┌────────────────────────────────────────────────────────────
# │                    ➕ Add New Student                     """)
#     student_id = input("🎓 Enter Student ID: ")
#     first_name = input("👤 Enter First Name: ")
#     middle_name = input("👤 Enter Middle Name (press Enter if none): ")
#     last_name = input("👤 Enter Last Name: ")
#     gender = input("👥 Enter Gender: ")
#     degree_program = input("📚 Enter Degree Program: ")
    
#     try:
#         cursor = conn.cursor()
        
#         # Insert the new student into member table
#         cursor.execute(
#             """INSERT INTO member 
#                (`Student Number`, `First Name`, `Middle Name`, `Last Name`, `Gender`, `Degree Program`) 
#                VALUES (?, ?, ?, ?, ?, ?)""",
#             (student_id, first_name, middle_name or None, last_name, gender, degree_program) # If middle name is empty, it will be Falsy. Since it's OR'd to None, it will only not be None if middle_name is not empty. https://www.freecodecamp.org/news/truthy-and-falsy-values-in-python/
#         )
#         conn.commit() # In mariadb-python, this saves data. This is different from MariaDB commits.
        
#         print("\n📝 Student Information to be added:")
#         print("┌────────────────────────────────────────────────────────────")
#         print(f"│ 🎓 ID: {student_id}")
#         print(f"│ 👤 Name: {first_name} {middle_name + ' ' if middle_name else ''}{last_name}") # If no middle name, it will not print anything.
#         print(f"│ 👥 Gender: {gender}")
#         print(f"│ 📚 Degree Program: {degree_program}")
#         print("└────────────────────────────────────────────────────────────")
#         print("\n✅ Student successfully added to database!")
        
#     except mariadb.Error as e:
#         print(f"\n❌ Error adding student: {e}")

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

def main(conn, student_id):
    while True:
        print_student_header()
        print_student_menu()
        choice = input("Enter your choice: ")
        
        if choice == "0":
            break
        elif choice == "1":
            view_organizations(conn, student_id)
        elif choice == "2":
            view_committees(conn, student_id)
        elif choice == "3":
            view_fees(conn, student_id)

if __name__ == "__main__": # Best practice for OOP in Python. When you import this file, it will not run automatically because __name__ will be the name of the file.
                            # However, when you run this file directly via python main.py, __name__ will be "__main__" and the code below will run.
    main()
