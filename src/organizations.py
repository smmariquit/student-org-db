import mariadb

from src import org_members, org_fees

# org_committees

def print_org_header():
    print("""┌────────────────────────────────────────────────────────────
│                 🏢 Organization Management                 """)

def print_org_menu():
    print("""📋 Organization Menu:
┌────────────────────────────────────────────────────────────
│ [1] ➕ Manage Members                                   
│ [2] ✏️  Manage Committees                                
│ [3] 🗑️  Manage Fees                                
│ [4] 👀 Delete Organization                                  
│ [0] ↩️  Back                                                
└────────────────────────────────────────────────────────────""")

def main(conn, organization_id):
    while True:
        print_org_header()
        print_org_menu()
        choice = input("Enter your choice: ")

        if choice == "0":
            break
        elif choice == "1":
            org_members.main(conn, organization_id)
        elif choice == "2":
            print("wala pa")
        elif choice == "3":
            org_fees.main(conn, organization_id)

if __name__ == "__main__": # Best practice for OOP in Python. When you import this file, it will not run automatically because __name__ will be the name of the file.
                            # However, when you run this file directly via python main.py, __name__ will be "__main__" and the code below will run.
    main()



# def add_organization(conn):
#     print("""┌────────────────────────────────────────────────────────────
# │                    ➕ Add New Organization                 """)
#     name = input("🏢 Enter Organization Name: ")
    
#     try:
#         cursor = conn.cursor()

#         cursor.execute("""INSERT INTO organization (`Organization Name`)
#                           VALUES (?)""",
#                        (name,))
#         conn.commit()

#         print("\n📝 Organization Information to be added:")
#         print("┌────────────────────────────────────────────────────────────")
#         print(f"│ 🏢 Name: {name}")
#         print("└────────────────────────────────────────────────────────────")
#         print("\n💾 Organization successfully added to database!")
    
#     except mariadb.Error as e:
#         print(f"\n❌ Error adding organization: {e}")

# def update_organization(conn):
#     print("""┌────────────────────────────────────────────────────────────
# │                     ✏️  Update Organization                 """)
#     org_id = input("🔍 Enter Organization ID to update: ")
    
#     try:
#         cursor = conn.cursor()

#         cursor.execute(
#             "SELECT * FROM organization WHERE `Organization ID` = ?",
#             (org_id,)
#         )
#         org = cursor.fetchone()

#         if org:
#             print("\n📋 Current Organization Information:")
#             print("┌────────────────────────────────────────────────────────────")
#             print(f"│ 🔢 ID: {org[0]}")
#             print(f"│ 🏢 Name: {org[1]}")
#             print("└────────────────────────────────────────────────────────────")
    
#             while True:
#                 print("\n📝 What would you like to update?")
#                 print("┌────────────────────────────────────────────────────────────")
#                 print("│ [1] 🏢 Name                                                ")
#                 print("│ [0] ↩️  Back                                                ")
#                 print("└────────────────────────────────────────────────────────────")
                
#                 choice = input("Enter your choice: ")
#                 if choice == "0":
#                     break
#                 elif choice == "1":
#                     new_name = input("Enter new Organization Name: ")
#                     cursor.execute(
#                         "UPDATE organization SET `Organization Name` = ? WHERE `Organization ID` = ?",
#                         (new_name, org_id))
#                     conn.commit()
#                     print(f"✅ Organization name updated to: {new_name}")
#         else:
#             print(f"\n❌ Organization with ID {org_id} not found!")

#     except mariadb.Error as e:
#         print(f"\n❌ Error updating organization: {e}")

# def delete_organization(conn):
#     print("""┌────────────────────────────────────────────────────────────
# │                     🗑️  Delete Organization                 """)
#     org_id = input("🔍 Enter Organization ID to delete: ")
    
#     try:
#         cursor = conn.cursor()
#         cursor.execute(
#             "SELECT * FROM organization WHERE `Organization ID` = ?",
#             (org_id,)
#         )
#         org = cursor.fetchone()

#         if org:
#             print("\n⚠️  Organization Information to be deleted:")
#             print("┌────────────────────────────────────────────────────────────")
#             print(f"│ 🔢 ID: {org[0]}")
#             print(f"│ 🏷️  Name: {org[1]}")
#             print("└────────────────────────────────────────────────────────────")
#             confirm = input("\n⚠️  Are you sure you want to delete this organization? (Y/N): ").upper()
#             if confirm == "Y":
#                 cursor.execute(
#                     "DELETE FROM organization WHERE `Organization ID` = ?",
#                     (org_id,)
#                 )
#                 conn.commit()
#                 print("✅ Organization successfully deleted from database!")
#         else:
#             print(f"\n❌ Organization with ID {org_id} not found!")

#     except mariadb.Error as e:
#         print(f"\n❌ Error deleting organization: {e}")

# def view_organizations(conn):
#     while True:
#         print("""┌────────────────────────────────────────────────────────────
# │                     👀 View Organizations                  """)
#         print("📋 View Options:")
#         print("┌────────────────────────────────────────────────────────────")
#         print("│ [1] 📋 View All Organizations                              ")
#         print("│ [0] ↩️  Back                                                ")
#         print("└────────────────────────────────────────────────────────────")
        
#         choice = input("Enter your choice: ")
#         if choice == "0":
#             break
#         elif choice == "1":
#             try:
#                 cursor = conn.cursor()

#                 cursor.execute("SELECT * FROM organization ORDER BY `Organization Name`")
#                 orgs = cursor.fetchall()

#                 if orgs:
#                     print("\n📋 Organization List:")
#                     print("┌──────────────────────────────────────────────────────────────┬──────────────┐")
#                     print("│ Organization Name                                            │ Org ID       │")
#                     print("├──────────────────────────────────────────────────────────────┼──────────────┤")

#                     for org in orgs:
#                         org_id = org[0]  
#                         org_name = org[1]    

#                         print(f"│ {org_name:<60} │ {org_id:<12} │")

#                     print("└──────────────────────────────────────────────────────────────┴──────────────┘\n")
#                 else:
#                     print("\nℹ️  No organizations found.\n")
            
#             except mariadb.Error as e:
#                 print(f"\n❌ Error viewing organizations: {e}")

# def main(conn):
#     while True:
#         print_org_header()
#         print_org_menu()
#         choice = input("Enter your choice: ")
        
#         if choice == "0":
#             break
#         elif choice == "1":
#             add_organization(conn)
#         elif choice == "2":
#             update_organization(conn)
#         elif choice == "3":
#             delete_organization(conn)
#         elif choice == "4":
#             view_organizations(conn)

# if __name__ == "__main__":
#     main()
