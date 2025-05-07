import mariadb
from typing import Optional # An Optional is like a Nullable in other languages. It's like a Maybe in Haskell or an Option in Rust. Here, we apply it in the Middle Name field because some people do not have middle names.

def print_student_header():
    print("""╔════════════════════════════════════════════════════════════╗
║                     👥 Student Management                  ║
╚════════════════════════════════════════════════════════════╝""")

def print_student_menu():
    print("""📋 Student Menu:
╔════════════════════════════════════════════════════════════╗
║ [1] ➕ Add Student                                         ║
║ [2] ✏️  Update Student                                      ║
║ [3] 🗑️  Delete Student                                      ║
║ [4] 👀 View Students                                       ║
║ [0] ↩️  Back                                                ║
╚════════════════════════════════════════════════════════════╝""")

def add_student():
    print("""╔════════════════════════════════════════════════════════════╗
║                     ➕ Add New Student                     ║
╚════════════════════════════════════════════════════════════╝""")
    student_number = input("📚 Enter Student Number: ")
    first_name = input("👤 Enter First Name: ")
    last_name = input("👤 Enter Last Name: ")
    gender = input("⚧ Enter Gender (M/F): ")
    degree_program = input("🎓 Enter Degree Program: ")
    batch = input("📅 Enter Batch Year (e.g. 2022): ")
    
    print("\n📝 Student Information to be added:")
    print("╔════════════════════════════════════════════════════════════")
    print(f"║ 📚 Student Number: {student_number}")
    print(f"║ 👤 Name: {first_name} {last_name}")
    print(f"║ ⚧ Gender: {gender}")
    print(f"║ 🎓 Degree Program: {degree_program}")
    print(f"║ 📅 Batch: {batch}")
    print("╚════════════════════════════════════════════════════════════")
    print("\n💾 Student would be added to database here.")

def update_student():
    print("""╔════════════════════════════════════════════════════════════╗
║                     ✏️  Update Student                      ║
╚════════════════════════════════════════════════════════════╝""")
    student_id = input("🔍 Enter Student ID to update: ")
    
    print("\n📋 Current Student Information:")
    print("╔════════════════════════════════════════════════════════════╗")
    print(f"║ 📚 Student Number: 2023-12345")
    print(f"║ 👤 Name: John Doe")
    print(f"║ ⚧ Gender: M")
    print(f"║ 🎓 Degree Program: BS Computer Science")
    print(f"║ 📅 Batch: 2023")
    print("╚════════════════════════════════════════════════════════════╝")
    
    while True:
        print("\n📝 What would you like to update?")
        print("╔════════════════════════════════════════════════════════════╗")
        print("║ [1] 📚 Student Number                                      ║")
        print("║ [2] 👤 Name                                                ║")
        print("║ [3] ⚧ Gender                                               ║")
        print("║ [4] 🎓 Degree Program                                      ║")
        print("║ [5] 📅 Batch                                               ║")
        print("║ [0] ↩️  Back                                                ║")
        print("╚════════════════════════════════════════════════════════════╝")
        
        choice = input("\n👉 Enter your choice: ")
        
        if choice == "0":
            break
            
        if choice == "1":
            new_number = input("📚 Enter new Student Number: ")
            print(f"✅ Student number would be updated to: {new_number}")
        elif choice == "2":
            first_name = input("👤 Enter new First Name: ")
            last_name = input("👤 Enter new Last Name: ")
            print(f"✅ Name would be updated to: {first_name} {last_name}")
        elif choice == "3":
            new_gender = input("⚧ Enter new Gender (M/F): ").upper()
            print(f"✅ Gender would be updated to: {new_gender}")
        elif choice == "4":
            new_program = input("🎓 Enter new Degree Program: ")
            print(f"✅ Degree program would be updated to: {new_program}")
        elif choice == "5":
            new_batch = input("📅 Enter new Batch Year: ")
            print(f"✅ Batch would be updated to: {new_batch}")
        
        print("💾 Update would be saved to database here.")

def delete_student():
    print("""╔════════════════════════════════════════════════════════════╗
║                     🗑️  Delete Student                      ║
╚════════════════════════════════════════════════════════════╝""")
    student_id = input("🔍 Enter Student ID to delete: ")
    
    print("\n⚠️ Student Information to be deleted:")
    print("╔════════════════════════════════════════════════════════════╗")
    print(f"║ 📚 Student Number: 2023-12345")
    print(f"║ 👤 Name: John Doe")
    print(f"║ ⚧ Gender: M")
    print(f"║ 🎓 Degree Program: BS Computer Science")
    print(f"║ 📅 Batch: 2023")
    print("╚════════════════════════════════════════════════════════════╝")
    
    confirm = input("\n⚠️ Are you sure you want to delete this student? (Y/N): ").upper()
    if confirm == "Y":
        print("🗑️ Student would be deleted from database here.")

def view_students():
    while True:
        print("""╔════════════════════════════════════════════════════════════╗
║                     👀 View Students                       ║
╚════════════════════════════════════════════════════════════╝""")
        print("📋 View Options:")
        print("╔════════════════════════════════════════════════════════════╗")
        print("║ [1] 📋 Print All Students                                 ║")
        print("║ [2] 🔍 Find Student by ID                                 ║")
        print("║ [3] 🏢 Filter by Organization                            ║")
        print("║ [4] 📅 Filter by Batch                                   ║")
        print("║ [0] ↩️  Back                                                ║")
        print("╚════════════════════════════════════════════════════════════╝")
        
        choice = input("\n👉 Enter your choice: ")
        
        if choice == "0":
            break
            
        if choice == "1":
            print("\n📋 Sample Student List:")
            print("╔════════════════════════════════════════════════════════════╗")
            print("║ 🔢 ID: 1")
            print("║ 📚 Student Number: 2023-12345")
            print("║ 👤 Name: John Doe")
            print("║ ⚧ Gender: M")
            print("║ 🎓 Degree Program: BS Computer Science")
            print("║ 📅 Batch: 2023")
            print("╚════════════════════════════════════════════════════════════╝")
            
            print("\n╔════════════════════════════════════════════════════════════╗")
            print("║ 🔢 ID: 2")
            print("║ 📚 Student Number: 2023-12346")
            print("║ 👤 Name: Jane Smith")
            print("║ ⚧ Gender: F")
            print("║ 🎓 Degree Program: BS Information Technology")
            print("║ 📅 Batch: 2023")
            print("╚════════════════════════════════════════════════════════════╝")
                
        elif choice == "2":
            student_id = input("🔍 Enter Student ID: ")
            print(f"\n🔍 Searching for student with ID: {student_id}")
            print("\n📋 Student Information:")
            print("╔════════════════════════════════════════════════════════════╗")
            print("║ 📚 Student Number: 2023-12345")
            print("║ 👤 Name: John Doe")
            print("║ ⚧ Gender: M")
            print("║ 🎓 Degree Program: BS Computer Science")
            print("║ 📅 Batch: 2023")
            print("╚════════════════════════════════════════════════════════════╝")
                
        elif choice == "3":
            org_id = input("🏢 Enter Organization ID: ")
            print(f"\n👥 Students in Organization {org_id}:")
            print("╔════════════════════════════════════════════════════════════╗")
            print("║ 🔢 ID: 1")
            print("║ 📚 Student Number: 2023-12345")
            print("║ 👤 Name: John Doe")
            print("║ ⚧ Gender: M")
            print("║ 🎓 Degree Program: BS Computer Science")
            print("║ 📅 Batch: 2023")
            print("╚════════════════════════════════════════════════════════════╝")
                
        elif choice == "4":
            batch = input("📅 Enter Batch Year: ")
            print(f"\n👥 Students in Batch {batch}:")
            print("╔════════════════════════════════════════════════════════════╗")
            print("║ 🔢 ID: 1")
            print("║ 📚 Student Number: 2023-12345")
            print("║ 👤 Name: John Doe")
            print("║ ⚧ Gender: M")
            print("║ 🎓 Degree Program: BS Computer Science")
            print("║ 📅 Batch: 2023")
            print("╚════════════════════════════════════════════════════════════╝")

def main():
    while True:
        print_student_header()
        print_student_menu()
        
        choice = input("\n👉 Enter your choice: ")
        
        if choice == "0":
            break
            
        if choice == "1":
            add_student()
        elif choice == "2":
            update_student()
        elif choice == "3":
            delete_student()
        elif choice == "4":
            view_students()
        else:
            print("❌ Invalid choice! Please try again.")
