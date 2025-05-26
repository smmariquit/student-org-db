import mariadb

def print_membership_header():
    print("""┌────────────────────────────────────────────────────────────
│                 👥 Membership Management                     """)

def print_membership_menu():
    print(""" 📋 Membership Menu:
┌────────────────────────────────────────────────────────────
│ [1] ➕ Add Member                                        
│ [2] ✏️  Update Member                                     
│ [3] 🗑️  Remove Member                                     
│ [4] 💰 View Members                                 
│ [0] ↩️  Back                                                
└────────────────────────────────────────────────────────────""")
    
def print_membership_report_menu():
    print("""📋 View Membership Reports:
┌────────────────────────────────────────────────────────────
│ [1] 👥 Members by Role/Status/Gender/Program/Batch/Committee                                      
│ [2] 🚫 Executive Committee Members by Academic Year                                     
│ [3] 🕐 Role by Year                                   
│ [4] 💸 Active vs Inactive % for Last N Semesters     
│ [5] 💸 Alumni as of Date (YYYY-MM-DD)
│ [6] 💸 Members with Highest Debt                                 
│ [0] ↩️  Back                                                
└────────────────────────────────────────────────────────────""")
    
def print_member_records_menu():
    print("""📋 View Member Records:
┌────────────────────────────────────────────────────────────
│ [1] 👥 See Profile                                        
│ [2] 🚫 See Roles Over Time                                     
│ [3] 🕐 See Status Over Time                                     
│ [4] 💸 See Other Organizations                                   
│ [0] ↩️  Back                                                
└────────────────────────────────────────────────────────────""")
    
def print_view_all_members_menu():
    print("""📋 View All Members:
┌────────────────────────────────────────────────────────────
│ [1] 👥 View by Role                                       
│ [2] 🚫 View by Status                                   
│ [3] 🕐 View by Gender                                   
│ [4] 💸 View by Degree Program
│ [5] 💸 View by Batch
│ [6] 💸 View by Committeee                                          
│ [0] ↩️  Back                                                
└────────────────────────────────────────────────────────────""")
    
def add_member_menu():
    print("""📋 View Add Member:
┌────────────────────────────────────────────────────────────
│ [1] 👥 Add Member to Organization                                        
│ [2] 🚫 Add Member to Committee                                                                    
│ [0] ↩️  Back                                                
└────────────────────────────────────────────────────────────""")

# 
def add_org_member(conn, org_id):
    print("""┌────────────────────────────────────────────────────────────
│                    ➕ Add New Organization Member                     """)
    student_id = input("🎓 Enter Member Student ID: ")
    first_name = input("👤 Enter First Name: ")
    middle_name = input("👤 Enter Middle Name (press Enter if none): ")
    last_name = input("👤 Enter Last Name: ")
    gender = input("👥 Enter Gender: ")
    degree_program = input("📚 Enter Degree Program: ")
    acad_year = input("👤 Enter Academic Year: ")
    semester = input("👤 Enter Semester: ")
    role = input("👤 Enter Member Role: ")
    status = input("👤 Enter Member Status (Active/Inactive/etc.): ")

    try:
        cursor = conn.cursor()

        cursor.execute(
            """INSERT INTO joins
            (`Student Number`,
            `Organization ID`,
            `Academic Year`,
            `Semester`,
            `Role`,
            `Status`)
            VALUES (?, ?, ?, ?, ?, ?)""",
        (student_id, org_id, acad_year, semester, role, status))
        conn.commit()

        # if ever the student has multiple orgs (their record already exists in member db)
        cursor.execute(
            "SELECT * FROM member WHERE `Student Number` = ?",
            (student_id,)
        )

        student = cursor.fetchone();
        if not student:
            cursor.execute("""INSERT INTO member
                           (`Student Number`, 
                           `First Name`, 
                           `Middle Name`, 
                           `Last Name`, 
                           `Gender`,
                           `Degree Program`)
                           VALUES (?, ?, ?, ?, ?, ?)""",
                           (student_id, first_name, middle_name, last_name, gender, degree_program))
        conn.commit()

        cursor.execute(
            """SELECT * FROM member_batch WHERE `Student ID` = ? 
                AND `Organization ID` = ?""",
            (student_id, org_id)
        )
        member = cursor.fetchone()
        # if member joins org for the first time, add their info to member_batch
        if not member: 
            cursor.execute(
                """INSERT INTO member_batch
                (`Student Number`,
                `Organization ID`,
                `Batch`)
                VALUES (?, ?, ?)""",
                (student_id, org_id, acad_year[:4])
            )
            conn.commit()
        
        print("\n✅ Member successfully added to database!")

        print("\n📝 Member Information to be added:")
        print("┌────────────────────────────────────────────────────────────")
        print(f"│ 🎓 Member ID: {student_id}")
        print(f"│ 🎓 Organization ID: {org_id}")
        print(f"│ 👤 Name: {first_name} {middle_name + ' ' if middle_name else ''}{last_name}") # If no middle name, it will not print anything.
        print(f"│ 👥 Gender: {gender}")
        print(f"│ 📚 Degree Program: {degree_program}")
        print(f"│ 📚 Academic Year: {acad_year}")
        print(f"│ 📚 Semester: {semester}")
        print(f"│ 📚 Role: {role}")
        print(f"│ 📚 Status: {status}")
        print("└────────────────────────────────────────────────────────────")
        
        
    except mariadb.Error as e:
        print(f"\n❌ Error adding member: {e}")
    
def update_org_member(conn, org_id):
    print("""┌────────────────────────────────────────────────────────────
│                     ✏️  Update Member                     """)
    member_id = input("Enter Member ID:")
    semester = input("Enter Semester (1st/2nd) : ")
    academic_year = input("Enter Academic Year (XXXX-XXXX): ")

    try:
        cursor = conn.cursor()

        cursor.execute(
            """SELECT * FROM joins WHERE
                `Student Number` = ? 
                AND `Organization ID` = ? 
                AND `Semester` = ? 
                AND `Academic Year` = ?""",
            (member_id, org_id, semester, academic_year)
        )

        member = cursor.fetchone()

        if member:
            print("\n📋 Current Member Information:")
            print("┌────────────────────────────────────────────────────────────")
            print(f"│ 🎓 Member ID: {member[0]}")
            print(f"│ 🎓 Organization ID: {member[1]}")
            print(f"│ 📚 Academic Year: {member[2]}")
            print(f"│ 📚 Semester: {member[3]}")
            print(f"│ 📚 Member Role: {member[4]}")
            print(f"│ 📚 Member Status: {member[5]}")
            print("└────────────────────────────────────────────────────────────")

            while True:
                print("\n📝 What would you like to update?")
                print("┌────────────────────────────────────────────────────────────")
                print("│ [1] 👤 Member Role                                                ")
                print("│ [2] 👤 Member Status                                              ")
                print("│ [0] ↩️  Back                                                ")
                print("└────────────────────────────────────────────────────────────")

                choice = input("Enter your choice: ")
                if choice == "0":
                    break
                elif choice == "1":
                    new_role = input("👤 Enter new Member Role: ")
                    cursor.execute(
                        """UPDATE joins
                        SET `Member Role` = ?
                        WHERE `Student Number` = ?
                            AND `Organization ID` = ?
                            AND `Academic Year` = ?
                            AND `Semester`= ?""",
                        (new_role, member_id, org_id, academic_year, semester)
                    )
                    conn.commit()
                    print(f"✅ Member role updated to: {new_role}")
                elif choice == "2":
                    new_status = input("👤 Enter new Member Status (Active/Inactive/Etc.): ")
                    cursor.execute(
                        """UPDATE joins
                        SET `Member Status` = ?
                        WHERE `Student Number` = ?
                            AND `Organization ID` = ?
                            AND `Academic Year` = ?
                            AND `Semester`= ?""",
                        (new_status, member_id, org_id, academic_year, semester)
                    )
                    conn.commit()
                    print(f"✅ Member Status updated to: {new_status}")
   
        else:
            print(f"\n❌ Fee with ID ({member_id}, {org_id}, {semester}, {academic_year}) not found!")

    except mariadb.Error as e:
        print(f"\n❌ Error updating fee: {e}")



# 3. Manage Memberships
#     → Input: Select Organization by ID or Name
#     1. Add Member
#         → Input: Student ID, Role, Status (active/inactive/etc.), Committee (if any), Semester, Academic Year
#     2. Update Member
#         → Input: Select Member
#     3. Remove Member
#         → Input: Confirm removal (Y/N)
#     4. View Members
#       1. View Specific Member
#           → Input: Student ID
#           1. See Profile
#           2. See Roles Over Time
#           3. See Status Over Time
#           4. See Other Organizations
#           0. Back
#       2. View All Members
#           1. View by Role
#               → Input: Role name
#           2. View by Status
#               → Input: Status type
#           3. View by Gender
#               → Input: M or F
#           4. View by Degree Program
#               → Input: Program name/code
#           5. View by Batch
#               → Input: Year
#           6. View by Committee
#               → Input: Committee name
#           0. Back
#       3. View Reports
#           1. Members by Role/Status/Gender/Program/Batch/Committee (Report #1)
#           2. Executive Committee Members by Academic Year (Report #4)
#               → Input: Academic Year
#           3. Presidents (or Role) by Year (reverse chronological) (Report #5)
#               → Input: Role name
#           4. Active vs Inactive % for Last N Semesters (Report #7)
#               → Input: N (positive integer)
#           5. Alumni as of Date (Report #8)
#               → Input: Date (YYYY-MM-DD)
#           6. Members with Highest Debt (Report #10)
#               → Input: Semester, Academic Year
#           0. Back
#       0. Back
#     0. Back