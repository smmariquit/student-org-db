import mariadb

def print_fee_header():
    print("""┌────────────────────────────────────────────────────────────
│                 👥 Fee Management                     """)

def print_fee_menu():
    print(""" 📋 Fee Menu:
┌────────────────────────────────────────────────────────────
│ [1] ➕ Add Fee                                        
│ [2] ✏️  Update Fee                                     
│ [3] 🗑️  Delete Fee                                     
│ [4] 💰 Generate Financial Status  
│ [5] 📊 View Fee Reports
│ [6] 📊 View All Fees                                           
│ [0] ↩️  Back                                                
└────────────────────────────────────────────────────────────""")
    
def add_fee(conn, organization_id):
    print("""┌────────────────────────────────────────────────────────────
│                    ➕ Add New Fee                     """)
    member_id = input("Enter Member ID: ")
    fee_name = input("Enter Fee Name: ")
    due_date = input("Enter Due Date (YYYY-MM-DD): ")
    academic_year = input("Enter Academic Year (XXXX-XXXX): ")
    semester = input("Enter Semester (1st/2nd) : ")
    amount = input("Enter Amount: ")

    try:
        cursor = conn.cursor()
        
        # Insert the new fee into fee table
        cursor.execute(
            """INSERT INTO fee 
               (`Organization ID`, 
               `Student Number`, 
               `Fee Name`,
               `Due Date`,
               `Academic Year`, 
               `Status`,
               `Semester`,
               `Amount`) 
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            (organization_id,
             member_id, 
             fee_name,
             due_date,
             academic_year,
             "Unpaid", 
             semester, 
             amount)
        )
        conn.commit() # In mariadb-python, this saves data. This is different from MariaDB commits.
        
        print("\n📝 Fee Information to be added:")
        print("┌────────────────────────────────────────────────────────────")
        print(f"│ 🎓 Organization ID: {organization_id}")
        print(f"│ 🎓 Member ID: {member_id}")
        print(f"│ 🎓 Fee Name: {fee_name}")
        print(f"│ 👥 Due Date: {due_date}")
        print(f"│ 📚 Academic Year: {academic_year}")
        print(f"│ 📚 Status: Unpaid")
        print(f"│ 📚 Semester: {semester}")
        print(f"│ 📚 Amount: {amount}")
        print("└────────────────────────────────────────────────────────────")
        print("\n✅ Fee successfully added to database!")
        
    except mariadb.Error as e:
        print(f"\n❌ Error adding fee: {e}")

# works
def update_fee(conn, organization_id):
    print("""┌────────────────────────────────────────────────────────────
│                     ✏️  Update Fee                     """)
    fee_name = input("🔍 Enter Fee Name: ")
    member_id = input("Enter Member ID:")
    semester = input("Enter Semester (1st/2nd) : ")
    academic_year = input("Enter Academic Year (XXXX-XXXX): ")

    try: 
        cursor = conn.cursor()

        cursor.execute(
            """SELECT `Organization ID`, `Student Number`, `Fee Name`, `Due Date`, `Academic Year`, `Status`, `Semester`, `Amount` FROM fee WHERE `Fee Name` = ? 
                AND `Student Number` = ? 
                AND `Organization ID` = ? 
                AND `Semester` = ? 
                AND `Academic Year` = ?""",
            (fee_name, member_id, organization_id, semester, academic_year)
        )
        fee = cursor.fetchone()

        if fee:
            print("\n📋 Current Fee Information:")
            print("┌────────────────────────────────────────────────────────────")
            print(f"│ 🎓 Organization ID: {fee[0]}")
            print(f"│ 🎓 Member ID: {fee[1]}")
            print(f"│ 🎓 Fee Name: {fee[2]}")
            print(f"│ 👥 Due Date: {fee[3]}")
            print(f"│ 📚 Academic Year: {fee[4]}")
            print(f"│ 📚 Status: {fee[5]}")
            print(f"│ 📚 Semester: {fee[6]}")
            print(f"│ 📚 Amount: {fee[7]}")
            print("└────────────────────────────────────────────────────────────")

            while True:
                print("\n📝 What would you like to update?")
                print("┌────────────────────────────────────────────────────────────")
                print("│ [1] 👤 Due Date                                                ")
                print("│ [2] 👤 Status                                              ")
                print("│ [0] ↩️  Back                                                ")
                print("└────────────────────────────────────────────────────────────")

                choice = input("Enter your choice: ")
                if choice == "0":
                    break
                elif choice == "1":
                    new_due_date = input("👤 Enter new Fee Due Date (YYYY-MM-DD): ")
                    cursor.execute(
                        """UPDATE fee
                        SET `Due Date` = ?
                        WHERE `Fee Name` = ?
                            AND `Student Number` = ?
                            AND `Organization ID` = ?
                            AND `Academic Year` = ?
                            AND `Semester`= ?""",
                        (new_due_date, fee_name, member_id, organization_id, academic_year, semester)
                    )
                    conn.commit()
                    print(f"✅ Fee due date updated to: {new_due_date}")
                elif choice == "2":
                    new_status = input("👤 Enter new Fee Status (Paid/Unpaid/Pending): ")
                    cursor.execute(
                        """UPDATE fee
                        SET `Status` = ?
                        WHERE `Fee Name` = ?
                            AND `Student Number` = ?
                            AND `Organization ID` = ?
                            AND `Academic Year` = ?
                            AND `Semester`= ?""",
                        (new_status, fee_name, member_id, organization_id, academic_year, semester)
                    )
                    conn.commit()
                    print(f"✅ Fee status updated to: {new_status}")
   
        else:
            print(f"\n❌ Fee with ID ({fee_name}, {member_id}, {organization_id}, {semester}, {academic_year}) not found!")

    except mariadb.Error as e:
        print(f"\n❌ Error updating fee: {e}")

def delete_fee(conn, organization_id):
    while True:
        print("""┌────────────────────────────────────────────────────────────
│ 🗑️  What would you like to delete?                     """)
        print("┌────────────────────────────────────────────────────────────")
        print("│ [1] 👤 Delete Fee from Database                                                ")
        print("│ [2] 👤 Delete Fee for Singular Member                                              ")
        print("│ [0] 👤 Back                       ")
        print("└────────────────────────────────────────────────────────────")
        choice = input("Enter your choice: ")
        
        if choice == "0":
            break
        elif choice == "1":
            print("""┌────────────────────────────────────────────────────────────
│                    ➕ Delete Fee From Database                  """)
            fee_name = input("🔍 Enter Fee Name: ")
            try:
                cursor = conn.cursor()
                
                cursor.execute(
                    """SELECT * FROM fee
                        WHERE `Fee Name` = ?
                            AND `Organization ID` = ?""",
                    (fee_name, organization_id)
                )
                fees = cursor.fetchall()

                if fees:
                    print("\n📋 Fee Details")
                    print("┌──────────────┬────────────────┬──────────────────────┬────────────┬────────────────┬─────────┬──────────┬──────────┐")
                    print("│ Org ID       │ Student Number │ Fee Name             │ Due Date   │ Academic Year  │ Status  │ Semester │ Amount   │")
                    print("├──────────────┼────────────────┼──────────────────────┼────────────┼────────────────┼─────────┼──────────┼──────────┤")

                    for row in fees:
                        org_id = row[0]
                        student_number = row[1]
                        fee_name = row[2]
                        due_date = str(row[3])
                        academic_year = row[4]
                        status = row[5]
                        semester = row[6]
                        amount = float(row[7])  # Ensure it's a float for formatting

                        print(f"│ {org_id:<12} │ {student_number:<14} │ {fee_name:<20} │ {due_date:<10} │ {academic_year:<14} │ {status:<7} │ {semester:<8} │ ₱{amount:<7.2f} │")

                    print("└──────────────┴────────────────┴──────────────────────┴────────────┴────────────────┴─────────┴──────────┴──────────┘\n")

                    confirm = input("\n⚠️  Are you sure you want to delete this fee? (Y/N): ").upper()
                    if confirm == "Y":
                        cursor.execute(
                            """DELETE FROM fee
                                WHERE `Fee Name` = ?
                                    AND `Organization ID` = ?""",
                            (fee_name, organization_id)
                        )
                        conn.commit()
                        print("✅ Fee successfully deleted from database!")

                else:
                    print(f"\n❌ Fee with ID ({fee_name}, {organization_id}) not found!")
                    
            except mariadb.Error as e:
                print(f"\n❌ Error deleting fee: {e}")
        elif choice == "2":
            print("""┌────────────────────────────────────────────────────────────
│                    ➕ Delete Fee From Member               """)
            fee_name = input("🔍 Enter Fee Name: ")
            member_id = input("Enter Member ID: ")
            semester = input("Enter Semester (1st/2nd): ")
            academic_year = input("Enter Academic Year (XXXX-XXXX): ")
            try:
                cursor = conn.cursor()

                cursor.execute(
                    """SELECT * FROM fee 
                        WHERE `Fee Name` = ? 
                            AND `Student Number` = ? 
                            AND `Organization ID` = ?
                            AND `Semester` = ?
                            AND `Academic Year` = ?""",
                    (fee_name, member_id, organization_id, semester, academic_year)
                )
                fee = cursor.fetchone()

                if fee:
                    print("\n📋 Current Fee Information:")
                    print("┌────────────────────────────────────────────────────────────")
                    print(f"│ 🎓 Organization ID: {fee[0]}")
                    print(f"│ 🎓 Member ID: {fee[1]}")
                    print(f"│ 🎓 Fee Name: {fee[2]}")
                    print(f"│ 👥 Due Date: {fee[3]}")
                    print(f"│ 📚 Academic Year: {fee[4]}")
                    print(f"│ 📚 Status: {fee[5]}")
                    print(f"│ 📚 Semester: {fee[6]}")
                    print(f"│ 📚 Amount: {fee[7]}")
                    print("└────────────────────────────────────────────────────────────")
                    confirm = input("\n⚠️  Are you sure you want to delete this fee? (Y/N): ").upper()
                    if confirm == "Y":
                        cursor.execute(
                            """DELETE FROM fee
                            WHERE `Fee Name` = ?
                                AND `Student Number` = ?
                                AND `Organization ID` = ?
                                AND `Academic Year` = ?
                                AND `Semester`= ?""",
                            (fee_name, member_id, organization_id, academic_year, semester)
                        )
                        conn.commit()
                        print("✅ Fee successfully deleted from database!")

                else:
                    print(f"\n❌ Fee with ID ({fee_name}, {organization_id}) not found!")
                    
            except mariadb.Error as e:
                print(f"\n❌ Error deleting fee: {e}")

def generate_fin_status(conn, organization_id):
    print("""┌────────────────────────────────────────────────────────────
│                    ➕ Generate Organization Financial Status               """)
    
    semester = input("Enter Semester (1st/2nd) : ")
    academic_year = input("Enter Academic Year (XXXX-XXXX): ")
    
    try:
        cursor = conn.cursor()

        cursor.execute(
            "SELECT `Fee Name`, `Status`, `Amount` FROM fee WHERE `Semester` = ? AND `Academic Year` = ? AND `Organization ID` = ?",
            (semester, academic_year, organization_id)
        )
        fees = cursor.fetchall()
         
        if fees:
            
            paid = 0
            unpaid = 0
            paid_count = 0
            unpaid_count = 0

            for fee in fees:
                status = fee[1]
                amount = int(fee[2])

                if status == "Paid":
                    paid += amount
                    paid_count += 1
                else:
                    unpaid += amount
                    unpaid_count += 1
            # returns correct info
            print("""┌────────────────────────────────────────────────────────────
│        ➕ Organization Financial Status               """)  
            print("┌────────────────────────────────────────────────────────────")
            print(f"│ 🎓 Total Amount Unpaid: ₱{unpaid}, {unpaid_count} fee(s)")
            print(f"│ 🎓 Total Amount Paid: ₱{paid}, {paid_count} fee(s)")
            print(f"│ 🎓 Net Balance: ₱{paid-unpaid}")
            print("└────────────────────────────────────────────────────────────")
        
        else:
            print(f"\n❌ Fees within {semester} Semester, Academic Year {academic_year} not found!")

    except mariadb.Error as e:
        print(f"\n❌ Error fetching financial status: {e}")

def view_fee_reports(conn, organization_id):
    while True:
        print("""📋 View Fee Reports:
┌────────────────────────────────────────────────────────────
│ [1] 👥 Members with Unpaid Dues for Given Semester                                        
│ [2] 🚫 Members with Highest Debt for a Given Semester                                    
│ [3] 🕐 All Late Member Payments in a Given Semester                                     
│ [4] 💸 Total Paid and Unpaid Fees as of Date                                   
│ [0] ↩️  Back                                                
└────────────────────────────────────────────────────────────""")
        
        choice = input("Enter your choice: ")
        if choice == "0":
            break

        elif choice == "1":
            semester = input("Enter Semester (1st/2nd): ")
            academic_year = input("Enter Academic Year (XXXX-XXXX): ")

            try:
                cursor = conn.cursor()

                cursor.execute("""
                    CREATE OR REPLACE VIEW unpaid_fees_orgvu AS
                    SELECT f.`Organization ID`, m.`Student Number`, m.`Last Name`, m.`First Name`,
                           f.`Fee Name`, f.`Amount`, f.`Due Date`, f.`Status`
                    FROM member m
                    JOIN fee f ON m.`Student Number` = f.`Student Number`
                    WHERE f.`Status` = 'Unpaid' OR f.`Status` = 'Pending'
                      AND f.`Organization ID` = ?
                      AND f.`Academic Year` = ?
                      AND f.`Semester` = ?
                """, (organization_id, academic_year, semester))

                cursor.execute("SELECT * FROM unpaid_fees_orgvu")
                results = cursor.fetchall()
                # working, wonky lang display
                if not results:
                    print("\n📭 No unpaid fees found for that member.\n")
                else:
                    print("\n📋 Unpaid Dues Report:\n")
                    print("┌──────────────┬──────────────┬──────────────┬──────────────┬──────────────┬──────────┬──────────────┬────────────┐")
                    print("│ Org ID       │ Student No   │ Last Name    │ First Name   │ Fee Name     │ Amount   │ Due Date     │ Status     │")
                    print("├──────────────┼──────────────┼──────────────┼──────────────┼──────────────┼──────────┼──────────────┼────────────┤")
                    for row in results:
                        print(f"│ {row[0]:<12} │ {row[1]:<12} │ {row[2]:<12} │ {row[3]:<12} │ {row[4]:<12} │ ₱{str(row[5]):<7} │ {row[6]:<12} │ {row[7]:<10} │")
                    print("└──────────────┴──────────────┴──────────────┴──────────────┴──────────────┴──────────┴──────────────┴────────────┘\n")

            except mariadb.Error as e:
                print(f"\n❌ Error fetching report: {e}")
        # TODO: members with highest debt in semester
        elif choice == "2":
            member_id = input("Enter member id: ")

            try: 
                cursor = conn.cursor()

            except mariadb.Error as e:
                print(f"\n❌ Error fetching report: {e}")

        elif choice == "3":
            organization_id = input("Enter Organization ID: ")
            semester = input("Enter Semester (1st/2nd): ")
            academic_year = input("Enter Academic Year (XXXX-XXXX): ")
            
            try:
                cursor = conn.cursor()
                cursor.execute(
                    """CREATE OR REPLACE VIEW late_paymentsvu AS
                        SELECT 
                            f.`Fee Name` AS fee_name, 
                            f.`Student Number` AS student_number, 
                            f.`Organization ID` AS organization_id, 
                            f.`Due Date` AS due_date, 
                            p.`Payment Late?` AS payment_late
                        FROM fee f
                        JOIN joins j ON f.`Student Number` = j.`Student Number`
                        JOIN payment p ON 
                            p.`Student Number` = f.`Student Number` AND
                            p.`Fee Name` = f.`Fee Name`
                        WHERE f.`Organization ID` = ?
                        AND p.`Payment Late?` = 1
                        AND j.`Academic Year` = ?
                        AND j.`Semester` = ?""",
                        (organization_id, academic_year, semester))
                
                cursor.execute("SELECT * FROM late_paymentsvu")
                results = cursor.fetchall()

                if results:
                    print("\n📋 Late Payments in the Given Semester")
                    print("┌─────────────────────┬──────────────┬──────────────┬────────────┬──────────────┐")
                    print("│ Fee Name            │ Student #    │ Org ID       │ Due Date   │ Late?        │")
                    print("├─────────────────────┼──────────────┼──────────────┼────────────┼──────────────┤")

                    for row in results:
                        fee_name = row[0]
                        student_number = row[1]
                        org_id = row[2]
                        due_date = str(row[3])
                        late = "Yes" if row[4] else "No"
                        
                        print(f"│ {fee_name:<20} │ {student_number:<12} │ {org_id:<12} │ {due_date:<10} │ {late:<12} │")

                    print("└─────────────────────┴──────────────┴──────────────┴────────────┴──────────────┘\n")
                else:
                    print("\nℹ️  No late payments found for the given filters.\n")
            
            except mariadb.Error as e:
                print(f"\n❌ Error fetching report: {e}")
            
        elif choice == "4":
            organization_id = input("Enter Organization ID: ")
            date = input("Enter Date (YYYY-MM-DD): ")
            
            try:
                cursor = conn.cursor()

                cursor.execute(
                    """CREATE OR REPLACE VIEW org_feesvu(organization_name, organization_id, fee_name, amount, due_date, academic_year, semester)
                            AS SELECT o.`Organization Name`, o.`Organization ID`, f.`Fee Name`, f.`Amount`, f.`Due Date`, f.`Academic Year`, f.`Semester`
                            FROM organization o
                            JOIN fee f ON o.`Organization ID` = f.`Organization ID`
                            WHERE o.`Organization ID` = ?
                                AND f.`Due Date` <= ?""",
                                (organization_id, date))
                
                cursor.execute("SELECT * FROM org_feesvu")
                results = cursor.fetchall()

                # working
                if results:
                    print("\n📋 Organization Fees Due On or Before Given Date")
                    print("┌────────────────────────┬──────────────┬──────────────────────┬──────────┬────────────┬────────────────┬────────────┐")
                    print("│ Organization Name      │ Org ID       │ Fee Name             │ Amount   │ Due Date   │ Academic Year  │ Semester   │")
                    print("├────────────────────────┼──────────────┼──────────────────────┼──────────┼────────────┼────────────────┼────────────┤")

                    for row in results:
                        org_name = row[0]
                        org_id = row[1]
                        fee_name = row[2]
                        amount = float(row[3])
                        due_date = str(row[4])
                        acad_year = row[5]
                        semester = row[6]
                        
                        print(f"│ {org_name:<24} │ {org_id:<12} │ {fee_name:<20} │ ₱{amount:<7.2f} │ {due_date:<10} │ {acad_year:<14} │ {semester:<10} │")

                    print("└────────────────────────┴──────────────┴──────────────────────┴──────────┴────────────┴────────────────┴────────────┘\n")
                else:
                    print("\nℹ️  No fees found for the given organization and date.\n")
            except mariadb.Error as e:
                print(f"\n❌ Error fetching report: {e}")

def main(conn, organization_id):
    while True:
        #organization_id = organization_auth(conn)
        print_fee_header()
        print_fee_menu()
        choice = input("Enter your choice: ")

        if choice == "0":
            break
        elif choice == "1":
            add_fee(conn, organization_id)
        elif choice == "2":
            update_fee(conn, organization_id)
        elif choice == "3":
            delete_fee(conn, organization_id)
        elif choice == "4":
            view_fee_reports(conn, organization_id)
        elif choice == "5":
            generate_fin_status(conn, organization_id)


if __name__ == "__main__": # Best practice for OOP in Python. When you import this file, it will not run automatically because __name__ will be the name of the file.
                            # However, when you run this file directly via python main.py, __name__ will be "__main__" and the code below will run.
    main()

#     3. Manage Fees
#         1. View Fee Reports
#             1. Members with Unpaid Dues for Given Semester (Report #2)
#             2. Late Payments in Given Semester (Report #6)
#             3. Total Paid and Unpaid Fees as of Date (Report #9)
#             4. View members with highest debt for a given semester (Report #10) 
#         2. Add Payment
#         3. Update Fee
#         4. Generate Organization Financial Report
#         5. Delete Fee 
#             1. Delete Fee From member
#             2. Delete Fee from database