import mariadb

def print_admin_header():
    print("""┌────────────────────────────────────────────────────────────
│                 👨‍💼 Admin Management                     """)

def print_admin_menu():
    print("""📋 Admin Menu:
┌────────────────────────────────────────────────────────────
│ [1] 🏢 Manage Organizations
│ [2] 👥 Manage Members
│ [0] ↩️  Back                                                
└────────────────────────────────────────────────────────────""")

def manage_organizations(conn):
    while True:
        print("""📋 Organization Management:
┌────────────────────────────────────────────────────────────
│ [1] ➕ Add Organization
│ [2] ✏️  Update Organization
│ [3] 🗑️  Delete Organization
│ [4] 👀 View Organizations
│ [0] ↩️  Back                                                
└────────────────────────────────────────────────────────────""")
        
        choice = input("Enter your choice: ")
        if choice == "0":
            break
        elif choice == "1":
            add_organization(conn)
        elif choice == "2":
            update_organization(conn)
        elif choice == "3":
            delete_organization(conn)
        elif choice == "4":
            view_organizations(conn)

def add_organization(conn):
    print("""┌────────────────────────────────────────────────────────────
│                    ➕ Add Organization                     """)
    
    org_id = input("🔢 Enter Organization ID: ")
    org_name = input("🏢 Enter Organization Name: ")
    
    try:
        cursor = conn.cursor()
        cursor.execute(
            """INSERT INTO organization 
            (`Organization ID`, `Organization Name`) 
            VALUES (?, ?)""",
            (org_id, org_name)
        )
        conn.commit()
        print("\n✅ Organization successfully added!")
        
        print("\n📝 Organization Information:")
        print("┌────────────────────────────────────────────────────────────")
        print(f"│ 🔢 ID: {org_id}")
        print(f"│ 🏢 Name: {org_name}")
        print("└────────────────────────────────────────────────────────────")
        
    except mariadb.Error as e:
        print(f"\n❌ Error adding organization: {e}")

def update_organization(conn):
    print("""┌────────────────────────────────────────────────────────────
│                    ✏️  Update Organization                     """)
    
    org_id = input("🔍 Enter Organization ID to update: ")
    
    try:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM organization WHERE `Organization ID` = ?",
            (org_id,)
        )
        org = cursor.fetchone()
        
        if org:
            print("\n📋 Current Organization Information:")
            print("┌────────────────────────────────────────────────────────────")
            print(f"│ 🔢 ID: {org[0]}")
            print(f"│ 🏢 Name: {org[1]}")
            print("└────────────────────────────────────────────────────────────")
            
            new_name = input("🏢 Enter new Organization Name: ")
            cursor.execute(
                "UPDATE organization SET `Organization Name` = ? WHERE `Organization ID` = ?",
                (new_name, org_id)
            )
            conn.commit()
            print(f"✅ Organization name updated to: {new_name}")
        else:
            print(f"\n❌ Organization with ID {org_id} not found!")
            
    except mariadb.Error as e:
        print(f"\n❌ Error updating organization: {e}")

def delete_organization(conn):
    print("""┌────────────────────────────────────────────────────────────
│                    🗑️  Delete Organization                     """)
    
    org_id = input("🔍 Enter Organization ID to delete: ")
    
    try:
        cursor = conn.cursor()
        
        # Get organization info before deletion
        cursor.execute(
            "SELECT * FROM organization WHERE `Organization ID` = ?",
            (org_id,)
        )
        org = cursor.fetchone()
        
        if org:
            print("\n⚠️  Organization Information to be deleted:")
            print("┌────────────────────────────────────────────────────────────")
            print(f"│ 🔢 ID: {org[0]}")
            print(f"│ 🏢 Name: {org[1]}")
            print("└────────────────────────────────────────────────────────────")
            
            confirm = input("\n⚠️  Are you sure you want to delete this organization? (Y/N): ").upper()
            if confirm == "Y":
                # supposedly idelete muna related records
                cursor.execute("DELETE FROM organization WHERE `Organization ID` = ?", (org_id,))
                conn.commit()
                print("✅ Organization successfully deleted!")
        else:
            print(f"\n❌ Organization with ID {org_id} not found!")
            
    except mariadb.Error as e:
        print(f"\n❌ Error deleting organization: {e}")

def view_organizations(conn):
    print("""┌────────────────────────────────────────────────────────────
│                    👀 View Organizations                     """)
    
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM organization ORDER BY `Organization ID`")
        organizations = cursor.fetchall()
        
        if organizations:
            print("\n📋 Organization List:")
            for org in organizations:
                print("┌────────────────────────────────────────────────────────────")
                print(f"│ 🔢 ID: {org[0]}")
                print(f"│ 🏢 Name: {org[1]}")
                print("└────────────────────────────────────────────────────────────")
        else:
            print("\n📋 No organizations found.")
            
    except mariadb.Error as e:
        print(f"\n❌ Error viewing organizations: {e}")

def manage_members(conn):
    while True:
        print("""📋 Member Management:
┌────────────────────────────────────────────────────────────
│ [1] 👥 View All Members
│ [2] 👥 Add Member
│ [3] 👥 Delete Member
│ [0] ↩️  Back                                                
└────────────────────────────────────────────────────────────""")
        
        choice = input("Enter your choice: ")
        if choice == "0":
            break
        elif choice == "1":
            view_all_members(conn)
        elif choice == "2":
            add_member(conn)
        elif choice == "3":
            delete_member(conn)

def add_member(conn):
    print("""┌────────────────────────────────────────────────────────────
│                    ➕ Add Member                     """)
    
    student_number = input("🔢 Enter Student Number: ")
    first_name = input("👤 Enter First Name: ") 
    middle_name = input("👤 Enter Middle Name: ")
    last_name = input("👤 Enter Last Name: ")
    gender = input("👥 Enter Gender: ")
    degree_program = input("🎓 Enter Degree Program: ") 
    
    try:
        cursor = conn.cursor()
        cursor.execute(
            """INSERT INTO member 
            (`Student Number`, `First Name`, `Middle Name`, `Last Name`, `Gender`, `Degree Program`) 
            VALUES (?, ?, ?, ?, ?, ?)""",   
            (student_number, first_name, middle_name, last_name, gender, degree_program)
        )
        conn.commit()
        print("\n✅ Member successfully added!")    
        
        print("\n📝 Member Information:")
        print("┌────────────────────────────────────────────────────────────")
        print(f"│ 🔢 Student Number: {student_number}")
        print(f"│ 👤 Name: {first_name} {middle_name + ' ' if middle_name else ''}{last_name}")
        print(f"│ 👥 Gender: {gender}")
        print(f"│ 📚 Degree Program: {degree_program}")
        print("└────────────────────────────────────────────────────────────")
    except mariadb.Error as e:
        print(f"\n❌ Error adding member: {e}")

def delete_member(conn):
    print("""┌────────────────────────────────────────────────────────────
│                     🗑️  Delete Member                     """)
    
    student_number = input("🔢 Enter Student Number to delete: ")
    
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM member WHERE `Student Number` = ?", (student_number,))
        conn.commit()
        if cursor.rowcount > 0: # rowcount is the number of rows affected by the query
            print("✅ Member successfully deleted!")    
        else:
            print(f"\n❌ Member with Student Number {student_number} not found!")
    except mariadb.Error as e:
        print(f"\n❌ Error deleting member: {e}")   

def view_all_members(conn):
    print("""┌────────────────────────────────────────────────────────────
│                    👥 View All Members                     """)
    
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT m.*, mb.`Batch`, o.`Organization Name`
            FROM member m
            LEFT JOIN member_batch mb ON m.`Student Number` = mb.`Student Number`
            LEFT JOIN organization o ON mb.`Organization ID` = o.`Organization ID`
            ORDER BY m.`Student Number`
        """)
        members = cursor.fetchall()
        
        if members:
            print("\n📋 Member List:")
            for member in members:
                print("┌────────────────────────────────────────────────────────────")
                print(f"│ 🎓 Student Number: {member[0]}")
                print(f"│ 👤 Name: {member[1]} {member[2] + ' ' if member[2] else ''}{member[3]}")
                print(f"│ 👥 Gender: {member[4]}")
                print(f"│ 📚 Degree Program: {member[5]}")
                if member[6]:  # Batch
                    print(f"│ 📅 Batch: {member[6]}")
                if member[7]:  # Organization Name
                    print(f"│ 🏢 Organization: {member[7]}")
                print("└────────────────────────────────────────────────────────────")
        else:
            print("\n📋 No members found.")
            
    except mariadb.Error as e:
        print(f"\n❌ Error viewing members: {e}")

def main(conn):
    while True:
        print_admin_header()
        print_admin_menu()
        choice = input("Enter your choice: ")
        
        if choice == "0":
            break
        elif choice == "1":
            manage_organizations(conn)
        elif choice == "2":
            manage_members(conn)

if __name__ == "__main__":
    main()
