import mariadb

def print_membership_header():
    print("""┌────────────────────────────────────────────────────────────
│                 👥 Membership Management                     """)

def print_membership_menu():
    print(""" 📋 Membership Menu:
┌────────────────────────────────────────────────────────────
│ [1] ➕ Add Member  
│ [2] ✏️  Update Membership                                            
│ [3] ✏️  Update Member                                     
│ [4] 🗑️  Remove Member                                     
│ [5] 💰 View Members                                 
│ [0] ↩️  Back                                                
└────────────────────────────────────────────────────────────""")

def organization_auth(conn):
    print("""┌────────────────────────────────────────────────────────────
│                 👥 Organization Management                     """)
    
    organization_id = input("🎓 Enter Organization ID: ")
    
    try:
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM organization WHERE `Organization ID` = ?", (organization_id,))
        organization = cursor.fetchone()
        if organization:
            return organization[0]
        else:
            print(f"\n❌ Organization with ID {organization_id} not found!")
            return None
    except mariadb.Error as e:
        print(f"\n❌ Error authenticating student: {e}")

def add_member(conn, organization_id):
    while True:
        print("""📋 Add Member Menu:
    ┌────────────────────────────────────────────────────────────
    │ [1] 👥 Add Member to Organization                                        
    │ [2] 🚫 Add Member to Committee                                                                    
    │ [0] ↩️  Back                                                
    └────────────────────────────────────────────────────────────""")
        choice = input("Enter your choice: ")
        if choice == "0":
            break
        elif choice == "1":
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
                (student_id, organization_id, acad_year, semester, role, status))
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
                        (student_id, organization_id)
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
                        (student_id, organization_id, acad_year[:4])
                    )
                    conn.commit()
                
                print("\n✅ Member successfully added to database!")

                print("\n📝 Member Information to be added:")
                print("┌────────────────────────────────────────────────────────────")
                print(f"│ 🎓 Member ID: {student_id}")
                print(f"│ 🎓 Organization ID: {organization_id}")
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
        elif choice == "2":
            # TODO: code for add member to committee
            print("wala pa")

def update_membership(conn, organization_id):
    print("""┌────────────────────────────────────────────────────────────
│                     ✏️  Renew Membership                     """)
    member_id = input("Enter Member ID: ")
    semester = input("Enter Semester (1st/2nd): ")
    academic_year = input("Enter Academic Year (XXXX-XXXX): ")
    member_role = input("Enter Member Role: ")
    member_status = input("Enter Member Status: ")

    try: 
        cursor = conn.cursor()

        cursor.execute(
            """SELECT * FROM joins WHERE
                `Student Number` = ? 
                AND `Organization ID` = ? 
                AND `Semester` = ? 
                AND `Academic Year` = ?""",
            (member_id, organization_id, semester, academic_year)
        )
        student = cursor.fetchone() # check if existing

        if student:
            try:
                cursor.execute(
                    """INSERT INTO joins
                    (`Student Number`,
                    `Organization ID`,
                    `Academic Year`,
                    `Semester`,
                    `Role`,
                    `Status`)
                    VALUES (?, ?, ?, ?, ?, ?)""",
                (member_id, organization_id, academic_year, semester, member_role, member_status))
                conn.commit()
            
            except mariadb.Error as e:
                print(f"\n❌ Error renewing membership: {e}")
        else:
            print("Student is not a member of this org!")
    
    except mariadb.Error as e:
        print(f"\n❌ Error renewing membership: {e}")
                
    
def update_org_member(conn, organization_id):
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
            (member_id, organization_id, semester, academic_year)
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
                        (new_role, member_id, organization_id, academic_year, semester)
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
                        (new_status, member_id, organization_id, academic_year, semester)
                    )
                    conn.commit()
                    print(f"✅ Member Status updated to: {new_status}")
   
        else:
            print(f"\n❌ Fee with ID ({member_id}, {organization_id}, {semester}, {academic_year}) not found!")

    except mariadb.Error as e:
        print(f"\n❌ Error updating fee: {e}")

def remove_org_member(conn, organization_id):
    while True:
        print("""📋 Remove Member Menu:
    ┌────────────────────────────────────────────────────────────
    │ [1] 👥 Remove Member from Organization                                    
    │ [2] 🚫 Remove Member from Committee                                                                   
    │ [0] ↩️  Back                                                
    └────────────────────────────────────────────────────────────""")
        choice = input("Enter your choice: ")
        if choice == "0":
            break
        elif choice == "1":
            # as if member never existed sa org
            print("""┌────────────────────────────────────────────────────────────
        │                     🗑️  Delete Student                     """)
            student_id = input("🔍 Enter Student ID to delete: ")
            
            try:
                cursor = conn.cursor()
                
                # Get student info before it gets deleted
                cursor.execute(
                    "SELECT * FROM member WHERE student_id = ?",
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
                    
                    confirm = input("\n⚠️  Are you sure you want to remove this student from your organization? (Y/N): ").upper()
                    if confirm == "Y":
                        cursor.execute("SELECT COUNT(*) FROM member_batch WHERE `Student Number` = ?")
                        org_count = cursor.fetchone()
                        
                        # if member only has 1 org (the one that wants to delete it), remove their data from the member table also
                        if org_count == 1:
                            cursor.execute("DELETE FROM member WHERE `Student Number` = ?", (student_id,))
                        
                        cursor.execute("DELETE FROM joins WHERE `Student Number` = ? AND `Organization ID` = ?", (student_id, organization_id))
                        cursor.execute("DELETE FROM member_batch WHERE `Student Number` = ? AND `Organization ID` = ?", (student_id, organization_id))
                        cursor.execute("DELETE FROM student_role WHERE `Student Number` = ? AND `Organization ID` = ?", (student_id, organization_id))
                        cursor.execute("DELETE FROM fee WHERE `Student Number` = ? AND `Organization ID` = ?", (student_id, organization_id))
                        cursor.execute("DELETE FROM payment WHERE `Student Number` = ? AND `Organization ID` = ?", (student_id, organization_id))

                        conn.commit()

                        print("✅ Student successfully deleted from database!")
                else:
                    print(f"\n❌ Student with ID {student_id} not found!")
                    
            except mariadb.Error as e:
                print(f"\n❌ Error deleting student: {e}")
        elif choice == "2":
            # TODO: code for removing member from committee
            print("wala pa")
            
def view_org_members(conn, organization_id):
    while True:
        print("""📋 View Member Menu:
┌────────────────────────────────────────────────────────────
│ [1] 👥 View All Members                                  
│ [2] 🚫 View Members by Category
│ [3] 🚫 View Roles for Every Academic Year
│ [4] 🚫 View Percentage of Active vs Inactive Members for the last N Semesters
│ [5] 🚫 View Alumni Members as of a Given Date                                        
│ [0] ↩️  Back                                                
└────────────────────────────────────────────────────────────""")
        choice = input("Enter your choice: ")
        if choice == "0":
            break
        elif choice == "1":
            try:
                cursor = conn.cursor()
                
                cursor.execute(
                    """SELECT `Organization ID`,
                    `Organization Name`,
                    `Student Number`,
                    `First Name`,
                    `Last Name`,
                    `Gender`,
                    `Degree Program`,
                    `Batch`
                    FROM member_batch mb 
                    JOIN organization o ON mb.`Organization ID` = o.`Organization ID`
                    JOIN member m ON mb.`Student Number` = m.`Student Number`
                    WHERE `Organization ID` = ?""",
                    (organization_id,)
                )
                results = cursor.fetchall()

                if results:
                    print("\n📋 Organization Member List")
                    print("┌────────────┬──────────────────────────────┬──────────────┬────────────┬────────────┬────────────┬────────────────────────────┬───────┐")
                    print("│ Org ID     │ Organization Name            │ Student #    │ First Name │ Last Name  │ Gender     │ Degree Program             │ Batch │")
                    print("├────────────┼──────────────────────────────┼──────────────┼────────────┼────────────┼────────────┼────────────────────────────┼───────┤")

                    for row in results:
                        org_id, org_name, student_num, first_name, last_name, gender, degree, batch = row
                        print(f"│ {org_id:<10} │ {org_name:<28} │ {student_num:<12} │ {first_name:<10} │ {last_name:<10} │ {gender:<10} │ {degree:<26} │ {batch:<5} │")

                    print("└────────────┴──────────────────────────────┴──────────────┴────────────┴────────────┴────────────┴────────────────────────────┴───────┘\n")
                else:
                    print("\nℹ️  No members found for this organization.\n")

            except mariadb.Error as e:
                print(f"\n❌ Error fetching members: {e}")
        elif choice == "2":
            while True:
                print("""📋 View Member by Category:
┌────────────────────────────────────────────────────────────
│ [1] 👥 Role                                  
│ [2] 🚫 Status
│ [3] 🚫 Gender
│ [4] 🚫 Degree Program
│ [5] 🚫 Batch 
│ [6] 🚫 Committee                                      
│ [0] ↩️  Back                                                
└────────────────────────────────────────────────────────────""")
                choice = input("Enter your choice: ")
                if choice == "0":
                    break
                elif choice == "1":
                    member_role = input("Enter member role: ")
                    try:
                        cursor = conn.cursor()

                        cursor.execute(
                            """SELECT o.`Organization ID`,
                            o.`Organization Name`,
                            j.`Role`,
                            m.`Student Number`,
                            m.`First Name`,
                            m.`Last Name`,
                            m.`Gender`,
                            m.`Degree Program`,
                            mb.`Batch`
                            FROM member_batch mb 
                            JOIN organization o ON mb.`Organization ID` = o.`Organization ID`
                            JOIN member m ON mb.`Student Number` = m.`Student Number`
                            JOIN joins j ON j.`Student Number` = m.`Student Number` AND o.`Organization ID`=j.`Organization ID`
                            WHERE `Organization ID` = ? AND `Member Role` = ?""",
                            (organization_id, member_role)
                        )
                        results = cursor.fetchall()

                        if results:
                            print(f"\n📋 Members with role '{member_role}' in Organization {organization_id}")
                            print("┌──────────────┬────────────────────────────┬────────────┬──────────────┬────────────┬────────────┬───────────────┬────────────┬────────┐")
                            print("│ Org ID       │ Organization Name          │ Role       │ Student #    │ First Name │ Last Name  │ Gender        │ Degree     │ Batch  │")
                            print("├──────────────┼────────────────────────────┼────────────┼──────────────┼────────────┼────────────┼───────────────┼────────────┼────────┤")

                            for row in results:
                                org_id, org_name, role, student_no, first_name, last_name, gender, degree, batch = row
                                print(f"│ {org_id:<12} │ {org_name:<26} │ {role:<10} │ {student_no:<12} │ {first_name:<10} │ {last_name:<10} │ {gender:<15} │ {degree:<12} │ {batch:<6} │")

                            print("└──────────────┴────────────────────────────┴────────────┴──────────────┴────────────┴────────────┴───────────────┴────────────┴────────┘\n")
                        else:
                            print(f"\nℹ️  No members with role '{member_role}' found in Organization {organization_id}.\n")


                    except mariadb.Error as e:
                        print(f"\n❌ Error fetching members: {e}")
                elif choice == "2":
                    member_status = input("Enter member status: ")

                    cursor = conn.cursor()
                
                    cursor.execute(
                            """SELECT o.`Organization ID`,
                            o.`Organization Name`,
                            j.`Status`,
                            m.`Student Number`,
                            m.`First Name`,
                            m.`Last Name`,
                            m.`Gender`,
                            m.`Degree Program`,
                            mb.`Batch`
                            FROM member_batch mb 
                            JOIN organization o ON mb.`Organization ID` = o.`Organization ID`
                            JOIN member m ON mb.`Student Number` = m.`Student Number`
                            JOIN joins j ON j.`Student Number` = m.`Student Number` AND o.`Organization ID`=j.`Organization ID`
                            WHERE `Organization ID` = ? AND `Status` = ?""",
                            (organization_id, member_status)
                        )
                    
                    results = cursor.fetchall()

                    if results:
                        print(f"\n📋 Members with status '{member_status}' in Organization {organization_id}")
                        print("┌──────────────┬────────────────────────────┬────────────┬──────────────┬────────────┬────────────┬───────────────┬────────────────────────────┬────────┐")
                        print("│ Org ID       │ Organization Name          │ Status     │ Student #    │ First Name │ Last Name  │ Gender        │ Degree Program              │ Batch  │")
                        print("├──────────────┼────────────────────────────┼────────────┼──────────────┼────────────┼────────────┼───────────────┼────────────────────────────┼────────┤")

                        for row in results:
                            org_id, org_name, status, student_no, first_name, last_name, gender, degree, batch = row
                            print(f"│ {org_id:<12} │ {org_name:<26} │ {status:<10} │ {student_no:<12} │ {first_name:<10} │ {last_name:<10} │ {gender:<15} │ {degree:<26} │ {batch:<6} │")

                        print("└──────────────┴────────────────────────────┴────────────┴──────────────┴────────────┴────────────┴───────────────┴────────────────────────────┴────────┘\n")
                    else:
                        print(f"\nℹ️  No members with status '{member_status}' found in Organization {organization_id}.\n")

                elif choice == "3":
                    member_gender = input("Enter member gender: ")

                    cursor = conn.cursor()
                
                    cursor.execute(
                        """SELECT `Organization ID`,
                        `Organization Name`,
                        `Student Number`,
                        `First Name`,
                        `Last Name`,
                        `Gender`,
                        `Degree Program`,
                        `Batch`
                        FROM member_batch mb 
                        JOIN organization o ON mb.`Organization ID` = o.`Organization ID`
                        JOIN member m ON mb.`Student Number` = m.`Student Number`
                        WHERE `Organization ID` = ? AND `Member Gender` = ?""",
                        (organization_id, member_gender)
                    )

                    results = cursor.fetchall()

                    if results:
                        print(f"\n📋 Members with role '{member_role}' in Organization {organization_id}")
                        print("┌──────────────┬────────────────────────────────────┬────────────┬──────────────┬────────────┬────────────┬───────────────┬────────────────────────────┬────────┐")
                        print("│ Org ID       │ Organization Name                  │ Role       │ Student #    │ First Name │ Last Name  │ Gender        │ Degree Program              │ Batch  │")
                        print("├──────────────┼────────────────────────────────────┼────────────┼──────────────┼────────────┼────────────┼───────────────┼────────────────────────────┼────────┤")

                        for row in results:
                            org_id, org_name, role, student_no, first_name, last_name, gender, degree, batch = row
                            print(f"│ {org_id:<12} │ {org_name:<36} │ {role:<10} │ {student_no:<12} │ {first_name:<10} │ {last_name:<10} │ {gender:<15} │ {degree:<26} │ {batch:<6} │")

                        print("└──────────────┴────────────────────────────────────┴────────────┴──────────────┴────────────┴────────────┴───────────────┴────────────────────────────┴────────┘\n")

                    else:
                        print(f"\nℹ️  No members with gender '{member_gender}' found in Organization {organization_id}.\n")
                
                elif choice == "4":
                    member_degprog = input("Enter member degree program: ")

                    cursor = conn.cursor()
                
                    cursor.execute(
                        """SELECT `Organization ID`,
                        `Organization Name`,
                        `Student Number`,
                        `First Name`,
                        `Last Name`,
                        `Gender`,
                        `Degree Program`,
                        `Batch`
                        FROM member_batch mb 
                        JOIN organization o ON mb.`Organization ID` = o.`Organization ID`
                        JOIN member m ON mb.`Student Number` = m.`Student Number`
                        WHERE `Organization ID` = ? AND `Degree Program` = ?""",
                        (organization_id, member_degprog)
                    )

                    results = cursor.fetchall()

                    if results:
                        print(f"\n📋 Members with Degree Program '{member_degprog}' in Organization {organization_id}")
                        print("┌──────────────┬────────────────────────────────────┬────────────┬──────────────┬────────────┬────────────┬───────────────┬────────────────────────────┬────────┐")
                        print("│ Org ID       │ Organization Name                  │ Role       │ Student #    │ First Name │ Last Name  │ Gender        │ Degree Program              │ Batch  │")
                        print("├──────────────┼────────────────────────────────────┼────────────┼──────────────┼────────────┼────────────┼───────────────┼────────────────────────────┼────────┤")

                        for row in results:
                            org_id, org_name, role, student_no, first_name, last_name, gender, degree, batch = row
                            print(f"│ {org_id:<12} │ {org_name:<36} │ {role:<10} │ {student_no:<12} │ {first_name:<10} │ {last_name:<10} │ {gender:<15} │ {degree:<26} │ {batch:<6} │")

                        print("└──────────────┴────────────────────────────────────┴────────────┴──────────────┴────────────┴────────────┴───────────────┴────────────────────────────┴────────┘\n")

                    else:
                        print(f"\nℹ️  No members with Degree Program '{member_degprog}' found in Organization {organization_id}.\n")

                    
                    


                    

        

# Batch, and Committee 
    

def main(conn):
    while True:
        organization_id = organization_auth(conn)
        print_membership_header()
        print_membership_menu()
        choice = input("Enter your choice: ")

        if choice == "0":
            break
        elif choice == "1":
            add_member(conn, organization_id)
        elif choice == "2":
            update_membership(conn, organization_id)
        elif choice == "3":
            update_org_member(conn, organization_id)
        elif choice == "4":
            remove_org_member(conn, organization_id)
        elif choice == "5":
            view_org_members(conn, organization_id)


if __name__ == "__main__": # Best practice for OOP in Python. When you import this file, it will not run automatically because __name__ will be the name of the file.
                            # However, when you run this file directly via python main.py, __name__ will be "__main__" and the code below will run.
    main()




#     1. Manage Members
#         1. Add New member
#         2. Renew membership
#         3. Update member
#             1. Update member role (org wide)
#             2. Update member information (tentative pa ano pwede iedit)
#         4. Remove member
#         5. View members
#             1. View all members 
#             2. View members by role, status, etc. (Report #1)
#             3. View roles for every academic year (Report #5) 
#             4. View percentage of active vs inactive members of a given organization for the last n semesters (Report #7)
#             5. View alumni members as of a given date (Report #8)