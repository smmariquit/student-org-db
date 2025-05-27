import mariadb

def print_committee_header():
    print("""┌────────────────────────────────────────────────────────────
│                 👥 Committee Management                     """)

def print_committee_menu():
    print(""" 📋 Committee Menu:
┌────────────────────────────────────────────────────────────
│ [1] ➕ Add Committee  
│ [2] 🗑️  Delete Committee                                            
│ [3] 👥 View Committees                                     
│ [0] ↩️  Back                                                
└────────────────────────────────────────────────────────────""")

def add_committee(conn, organization_id):
    print("""┌────────────────────────────────────────────────────────────
│                    ➕ Add New Committee                     """)
    
    committee_name = input("👥 Enter Committee Name: ")
    
    try:
        cursor = conn.cursor()
        
        # Check if committee already exists
        cursor.execute(
            """SELECT * FROM committee 
            WHERE `Organization ID` = ? AND `Committee Name` = ?""",
            (organization_id, committee_name)
        )
        
        if cursor.fetchone():
            print(f"\n❌ Committee '{committee_name}' already exists in this organization!")
            return
            
        # Add new committee
        cursor.execute(
            """INSERT INTO committee
            (`Organization ID`,
            `Committee Name`,
            VALUES (?, ?, ?)""",
            (organization_id, committee_name)
        )
        conn.commit()
        
        print("\n✅ Committee successfully added!")
        print("\n📝 Committee Information:")
        print("┌────────────────────────────────────────────────────────────")
        print(f"│ 🏢 Organization ID: {organization_id}")
        print(f"│ 👥 Committee Name: {committee_name}")
        print("└────────────────────────────────────────────────────────────")
        
    except mariadb.Error as e:
        print(f"\n❌ Error adding committee: {e}")

def delete_committee(conn, organization_id):
    print("""┌────────────────────────────────────────────────────────────
│                    🗑️  Delete Committee                     """)
    
    committee_name = input("👥 Enter Committee Name to delete: ")
    
    try:
        cursor = conn.cursor()
        
        # Check if committee exists
        cursor.execute(
            """SELECT * FROM committee 
            WHERE `Organization ID` = ? AND `Committee Name` = ?""",
            (organization_id, committee_name)
        )
        
        committee = cursor.fetchone()
        
        if not committee:
            print(f"\n❌ Committee '{committee_name}' not found in this organization!")
            return
            
        # Show committee info before deletion
        print("\n⚠️  Committee Information to be deleted:")
        print("┌────────────────────────────────────────────────────────────")
        print(f"│ 🏢 Organization ID: {committee[0]}")
        print(f"│ 👥 Committee Name: {committee[1]}")
        print("└────────────────────────────────────────────────────────────")
        
        # Confirm deletion
        confirm = input("\n⚠️  Are you sure you want to delete this committee? (Y/N): ").upper()
        if confirm == "Y":
            # Delete committee
            cursor.execute(
                """DELETE FROM committee 
                WHERE `Organization ID` = ? AND `Committee Name` = ?""",
                (organization_id, committee_name)
            )
            conn.commit()
            print("\n✅ Committee successfully deleted!")
        else:
            print("\n❌ Committee deletion cancelled.")
            
    except mariadb.Error as e:
        print(f"\n❌ Error deleting committee: {e}")

def view_committees(conn, organization_id):
    print("""┌────────────────────────────────────────────────────────────
│                    👥 View Committees                     """)
    
    try:
        cursor = conn.cursor()
        
        cursor.execute(
            """SELECT * FROM committee 
            WHERE `Organization ID` = ?
            ORDER BY `Committee Name`""",
            (organization_id,)
        )
        
        results = cursor.fetchall()
        
        if results:
            for row in results:
                print("┌────────────────────────────────────────────────────────────")
                print(f"│ 🏢 Organization ID: {row[0]}")
                print(f"│ 👥 Committee Name: {row[1]}")
                print("└────────────────────────────────────────────────────────────")
        else:
            print("\nℹ️  No committees found for this organization.")
            
    except mariadb.Error as e:
        print(f"\n❌ Error viewing committees: {e}")

def main(conn, organization_id):
    while True:
        print_committee_header()
        print_committee_menu()
        choice = input("Enter your choice: ")

        if choice == "0":
            break
        elif choice == "1":
            add_committee(conn, organization_id)
        elif choice == "2":
            delete_committee(conn, organization_id)
        elif choice == "3":
            view_committees(conn, organization_id)

if __name__ == "__main__":
    main() 