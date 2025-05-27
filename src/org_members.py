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

def add_member(conn, organization_id):
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
            `Member Role`,
            `Member Status`)
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
                """SELECT * FROM member_batch WHERE `Student Number` = ? 
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
                AND `Organization ID` = ?""",
            (member_id, organization_id)
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
                    `Member Role`,
                    `Member Status`)
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
                AND `Organization ID` = ?""",
            (member_id, organization_id)
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
    # as if member never existed sa org
    print("""┌────────────────────────────────────────────────────────────
│                     🗑️  Delete Student                     """)
    student_id = input("🔍 Enter Student ID to delete: ")
    
    try:
        cursor = conn.cursor()
        
        # Get student info before it gets deleted
        cursor.execute(
            "SELECT * FROM member WHERE `Student Number` = ?",
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
                cursor.execute("SELECT COUNT(*) FROM member_batch WHERE `Student Number` = ?", (student_id,))
                org_count = cursor.fetchone()
                
                # if member only has 1 org (the one that wants to delete it), remove their data from the member table also
                if org_count[0] == 1:
                    cursor.execute("DELETE FROM member WHERE `Student Number` = ?", (student_id,))
                    conn.commit()
                
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
        # WORKS
        elif choice == "1":
            try:
                cursor = conn.cursor()
                
                cursor.execute(
                    """SELECT o.`Organization ID`,
                    o.`Organization Name`,
                    m.`Student Number`,
                    m.`First Name`,
                    m.`Last Name`,
                    m.`Gender`,
                    m.`Degree Program`,
                    mb.`Batch`
                    FROM member_batch mb 
                    JOIN organization o ON mb.`Organization ID` = o.`Organization ID`
                    JOIN member m ON mb.`Student Number` = m.`Student Number`
                    WHERE o.`Organization ID` = ?""",
                    (organization_id,)
                )
                results = cursor.fetchall()

                if results:
                    for row in results:
                        print("┌────────────────────────────────────────────────────────────")
                        print(f"│ 🏢 Organization ID: {row[0]}")
                        print(f"│ 🏢 Organization Name: {row[1]}")
                        print(f"│ 💰 Student Number: {row[2]}")
                        print(f"│ 📅 First Name: {row[3]}")
                        print(f"│ 📚 Last Name: {row[4]}")
                        print(f"│ 🔃 Gender: {row[5]}")
                        print(f"│ 🗓️ Degree Program: {row[6]}")
                        print(f"│ 🗓️ Batch: {row[7]}")
                        print("└────────────────────────────────────────────────────────────")
                else:
                    print("\nℹ️  No members found for this organization.\n")

            except mariadb.Error as e:
                print(f"\n❌ Error fetching members: {e}")
        # 
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
                            j.`Member Role`,
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
                            WHERE o.`Organization ID` = ? AND j.`Member Role` = ?""",
                            (organization_id, member_role)
                        )
                        results = cursor.fetchall()

                        if results:
                            for row in results:
                                print("┌────────────────────────────────────────────────────────────")
                                print(f"│ 🏢 Organization ID: {row[0]}")
                                print(f"│ 🏢 Organization Name: {row[1]}")
                                print(f"│ 💰 Member Role: {row[2]}")
                                print(f"│ 📅 Student Number: {row[3]}")
                                print(f"│ 📚 First Name: {row[4]}")
                                print(f"│ 🔃 Last Name: {row[5]}")
                                print(f"│ 🗓️ Gender: {row[6]}")
                                print(f"│ 💳 Degree Program: {row[7]}")
                                print(f"│ 💳 Batch: {row[8]}")
                                print("└────────────────────────────────────────────────────────────")

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
                            j.`Member Status`,
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
                            WHERE o.`Organization ID` = ? AND j.`Member Status` = ?""",
                            (organization_id, member_status)
                        )
                    
                    results = cursor.fetchall()

                    if results:
                        for row in results:
                                print("┌────────────────────────────────────────────────────────────")
                                print(f"│ 🏢 Organization ID: {row[0]}")
                                print(f"│ 🏢 Organization Name: {row[1]}")
                                print(f"│ 💰 Member Status: {row[2]}")
                                print(f"│ 📅 Student Number: {row[3]}")
                                print(f"│ 📚 First Name: {row[4]}")
                                print(f"│ 🔃 Last Name: {row[5]}")
                                print(f"│ 🗓️ Gender: {row[6]}")
                                print(f"│ 💳 Degree Program: {row[7]}")
                                print(f"│ 💳 Batch: {row[8]}")
                                print("└────────────────────────────────────────────────────────────")

                    else:
                        print(f"\nℹ️  No members with status '{member_status}' found in Organization {organization_id}.\n")

                elif choice == "3":
                    member_gender = input("Enter member gender: ")

                    cursor = conn.cursor()
                
                    cursor.execute(
                        """SELECT o.`Organization ID`,
                        o.`Organization Name`,
                        m.`Student Number`,
                        m.`First Name`,
                        m.`Last Name`,
                        m.`Gender`,
                        m.`Degree Program`
                        FROM member_batch mb 
                        JOIN organization o ON mb.`Organization ID` = o.`Organization ID`
                        JOIN member m ON mb.`Student Number` = m.`Student Number`
                        WHERE o.`Organization ID` = ? AND m.`Gender` = ?""",
                        (organization_id, member_gender)
                    )

                    results = cursor.fetchall()

                    if results:
                        for row in results:
                                print("┌────────────────────────────────────────────────────────────")
                                print(f"│ 🏢 Organization ID: {row[0]}")
                                print(f"│ 🏢 Organization Name: {row[1]}")
                                print(f"│ 💰 Student Number: {row[2]}")
                                print(f"│ 📅 First Name: {row[3]}")
                                print(f"│ 📚 Last Name: {row[4]}")
                                print(f"│ 🔃 Gender: {row[5]}")
                                print(f"│ 🗓️ Degree Program: {row[6]}")
                                print("└────────────────────────────────────────────────────────────")

                    else:
                        print(f"\nℹ️  No members with gender '{member_gender}' found in Organization {organization_id}.\n")
                
                elif choice == "4":
                    member_degprog = input("Enter member degree program: ")

                    cursor = conn.cursor()
                
                    cursor.execute(
                        """SELECT o.`Organization ID`,
                        o.`Organization Name`,
                        m.`Student Number`,
                        m.`First Name`,
                        m.`Last Name`,
                        m.`Gender`,
                        m.`Degree Program`
                        FROM member_batch mb 
                        JOIN organization o ON mb.`Organization ID` = o.`Organization ID`
                        JOIN member m ON mb.`Student Number` = m.`Student Number`
                        WHERE o.`Organization ID` = ? AND m.`Degree Program` = ?""",
                        (organization_id, member_degprog)
                    )

                    results = cursor.fetchall()

                    if results:
                        for row in results:
                            print("┌────────────────────────────────────────────────────────────")
                            print(f"│ 🏢 Organization ID: {row[0]}")
                            print(f"│ 🏢 Organization Name: {row[1]}")
                            print(f"│ 💰 Student Number: {row[2]}")
                            print(f"│ 📅 First Name: {row[3]}")
                            print(f"│ 📚 Last Name: {row[4]}")
                            print(f"│ 🔃 Gender: {row[5]}")
                            print(f"│ 🗓️ Degree Program: {row[6]}")
                            print("└────────────────────────────────────────────────────────────")

                    else:
                        print(f"\nℹ️  No members with Degree Program '{member_degprog}' found in Organization {organization_id}.\n")

                elif choice == "5":
                    member_batch = input("Enter member batch (YYYY): ")

                    cursor = conn.cursor()
                
                    cursor.execute(
                        """SELECT o.`Organization ID`,
                        o.`Organization Name`,
                        m.`Student Number`,
                        m.`First Name`,
                        m.`Last Name`,
                        m.`Gender`,
                        m.`Degree Program`,
                        mb.`Batch`
                        FROM member_batch mb 
                        JOIN organization o ON mb.`Organization ID` = o.`Organization ID`
                        JOIN member m ON mb.`Student Number` = m.`Student Number`
                        WHERE o.`Organization ID` = ? AND mb.`Batch` = ?""",
                        (organization_id, member_batch)
                    )

                    results = cursor.fetchall()

                    if results:
                        for row in results:
                            print("┌────────────────────────────────────────────────────────────")
                            print(f"│ 🏢 Organization ID: {row[0]}")
                            print(f"│ 🏢 Organization Name: {row[1]}")
                            print(f"│ 💰 Student Number: {row[2]}")
                            print(f"│ 📅 First Name: {row[3]}")
                            print(f"│ 📚 Last Name: {row[4]}")
                            print(f"│ 🔃 Gender: {row[5]}")
                            print(f"│ 🗓️ Degree Program: {row[6]}")
                            print(f"│ 🗓️ Batch: {row[7]}")
                            print("└────────────────────────────────────────────────────────────")

                    else:
                        print(f"\nℹ️  No members with batch '{member_batch}' found in Organization {organization_id}.\n")
                elif choice == "6":
                    member_committee = input("Enter member committee: ")

                    cursor = conn.cursor()

                    cursor.execute(
                        """SELECT o.`Organization ID`,
                        o.`Organization Name`,
                        m.`Student Number`,
                        m.`First Name`,
                        m.`Last Name`,
                        m.`Gender`,
                        m.`Degree Program`,
                        sr.`Committee Name`
                        FROM student_role sr    
                        JOIN organization o ON sr.`Organization ID` = o.`Organization ID`
                        JOIN member m ON sr.`Student Number` = m.`Student Number`
                        WHERE o.`Organization ID` = ? AND sr.`Committee Name` = ?""",    
                        (organization_id, member_committee)
                    )

                    results = cursor.fetchall()

                    if results:
                        for row in results:
                            print("┌────────────────────────────────────────────────────────────")
                            print(f"│ 🏢 Organization ID: {row[0]}")
                            print(f"│ 🏢 Organization Name: {row[1]}")
                            print(f"│ 💰 Student Number: {row[2]}")
                            print(f"│ 📅 First Name: {row[3]}")
                            print(f"│ 📚 Last Name: {row[4]}")
                            print(f"│ 🔃 Gender: {row[5]}")
                            print(f"│ 🗓️ Degree Program: {row[6]}")
                            print(f"│ 🗓️ Committee: {row[7]}")
                            print(f"│ 🗓️ Academic Year: {row[8]}")
                            print("└────────────────────────────────────────────────────────────")
                    else:
                        print(f"\nℹ️  No members found in committee '{member_committee}' for Organization {organization_id}.\n")
        elif choice == "3":
            member_role = input("Enter member role: ")
            
            try:
                cursor = conn.cursor()
                cursor.execute("""CREATE OR REPLACE VIEW organization_rolevu
                               (student_number, 
                               last_name, 
                               first_name, 
                               role, 
                               academic_year)
                            AS SELECT m.`Student Number`, m.`Last Name`, m.`First Name`, j.`Member Role`, j.`Academic Year`
                            FROM member m
                            JOIN joins j ON m.`Student Number` = j.`Student Number`
                            WHERE j.`Member Role` = ?
                                AND j.`Organization ID` = ?
                            ORDER BY STR_TO_DATE(CONCAT(SUBSTRING_INDEX(j.`Academic Year`, '-', 1), '-01-01'), '%Y-%m-%d') DESC""",
                            (member_role, organization_id))
                cursor.execute("SELECT * FROM organization_rolevu")
                results = cursor.fetchall()
                if results:
                    for row in results:
                        print("┌────────────────────────────────────────────────────────────")
                        print(f"│ 🏢 Student Number: {row[0]}")
                        print(f"│ 🏢 Last Name: {row[1]}")
                        print(f"│ 💰 First Name: {row[2]}")
                        print(f"│ 📅 Role: {row[3]}")
                        print(f"│ 📚 Academic Year: {row[4]}")
                        print("└────────────────────────────────────────────────────────────")
                else:
                    print("\n❌ No members with that role found.\n")
            except mariadb.Error as e:
                print(f"\n❌ Error fetching data: {e}")
        elif choice == "5":
            try:
                cursor = conn.cursor()
                cursor.execute("""CREATE OR REPLACE VIEW alumnivu(student_number, first_name, last_name, organization_id, status) 
                    AS SELECT m.`Student Number`, m.`First Name`, m.`Last Name`, j.`Organization ID`, j.`Member Status`
                    FROM member m
                    JOIN joins j ON m.`Student Number` = j.`Student Number`
                    WHERE (j.`Student Number`, j.`Organization ID`, 
                        STR_TO_DATE(CONCAT(SUBSTRING_INDEX(j.`Academic Year`, '-', 1), 
                                            CASE j.`Semester` 
                                                WHEN '1st' THEN '-01-01' 
                                                WHEN '2nd' THEN '-08-01' 
                                                ELSE '-01-01' 
                                            END), '%Y-%m-%d')
                        ) IN (
                        SELECT 
                            j2.`Student Number`, 
                            j2.`Organization ID`,
                            MAX(STR_TO_DATE(CONCAT(SUBSTRING_INDEX(j2.`Academic Year`, '-', 1), 
                                                CASE j2.`Semester` 
                                                    WHEN '1st' THEN '-01-01' 
                                                    WHEN '2nd' THEN '-08-01' 
                                                    ELSE '-01-01' 
                                                END), '%Y-%m-%d'))
                        FROM joins j2
                        GROUP BY j2.`Student Number`, j2.`Organization ID`
                    )
                    AND j.`Member Status` = 'Alumni'
                    AND j.`Organization ID` = ?""",
                            (organization_id,))
                cursor.execute("SELECT * FROM alumnivu")
                results = cursor.fetchall()
                if results:
                    for row in results:
                        print("┌────────────────────────────────────────────────────────────")
                        print(f"│ 🏢 Student Number: {row[0]}")
                        print(f"│ 🏢 Last Name: {row[1]}")
                        print(f"│ 💰 First Name: {row[2]}")
                        print(f"│ 📅 Role: {row[3]}")
                        print(f"│ 📚 Academic Year: {row[4]}")
                        print("└────────────────────────────────────────────────────────────")
                else:
                    print("\n❌ No alumni members found.\n")
            except mariadb.Error as e:
                print(f"\n❌ Error fetching data: {e}")
        elif choice == "0":
            break

def main(conn, organization_id):
    while True:
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