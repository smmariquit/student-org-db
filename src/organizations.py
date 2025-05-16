import mariadb

def print_org_header():
    print("""┌────────────────────────────────────────────────────────────
│                 🏢 Organization Management                 """)

def print_org_menu():
    print("""📋 Organization Menu:
┌────────────────────────────────────────────────────────────
│ [1] ➕ Add Organization                                    
│ [2] ✏️  Update Organization                                 
│ [3] 🗑️  Delete Organization                                 
│ [4] 👀 View Organizations                                  
│ [0] ↩️  Back                                                
└────────────────────────────────────────────────────────────""")

def add_organization():
    print("""┌────────────────────────────────────────────────────────────
│                    ➕ Add New Organization                 """)
    name = input("🏢 Enter Organization Name: ")
    
    print("\n📝 Organization Information to be added:")
    print("┌────────────────────────────────────────────────────────────")
    print(f"│ 🏢 Name: {name}")
    print("└────────────────────────────────────────────────────────────")
    print("\n💾 <Insert database save>")

def update_organization():
    print("""┌────────────────────────────────────────────────────────────
│                     ✏️  Update Organization                 """)
    org_id = input("🔍 Enter Organization ID to update: ")
    
    print("\n📋 Current Organization Information:")
    print("┌────────────────────────────────────────────────────────────")
    print(f"│ 🔢 ID: 1")
    print(f"│ 🏢 Name: Alliance of Cat Students for Science UPLB")
    print("└────────────────────────────────────────────────────────────")
    
    while True:
        print("\n📝 What would you like to update?")
        print("┌────────────────────────────────────────────────────────────")
        print("│ [1] 🏢 Name                                                ")
        print("│ [0] ↩️  Back                                                ")
        print("└────────────────────────────────────────────────────────────")
        
        choice = input("Enter your choice: ")
        if choice == "0":
            break

def delete_organization():
    print("""┌────────────────────────────────────────────────────────────
│                     🗑️  Delete Organization                 """)
    org_id = input("🔍 Enter Organization ID to delete: ")
    
    print("\n⚠️  Organization Information to be deleted:")
    print("┌────────────────────────────────────────────────────────────")
    print(f"│ 🔢 ID: 1")
    print(f"│ 🏷️  Name: Alliance of Cat Students for Science UPLB")
    print("└────────────────────────────────────────────────────────────")

def view_organizations():
    while True:
        print("""┌────────────────────────────────────────────────────────────
│                     👀 View Organizations                  """)
        print("📋 View Options:")
        print("┌────────────────────────────────────────────────────────────")
        print("│ [1] 📋 View All Organizations                              ")
        print("│ [0] ↩️  Back                                                ")
        print("└────────────────────────────────────────────────────────────")
        
        choice = input("Enter your choice: ")
        if choice == "0":
            break
        elif choice == "1":
            print("\n📋 Sample Organization List:")
            print("┌────────────────────────────────────────────────────────────")
            print(f"│ 🔢 ID: 1")
            print(f"│ 🏢 Name: Alliance of Cat Students for Science UPLB")
            print("└────────────────────────────────────────────────────────────")
            
            print("\n┌────────────────────────────────────────────────────────────")
            print("│ 🔢 ID: 2")
            print("│ 🏢 Name: Young Squirrel Entrepreneurial Society")
            print("└────────────────────────────────────────────────────────────")

def main():
    while True:
        print_org_header()
        print_org_menu()
        choice = input("Enter your choice: ")
        
        if choice == "0":
            break
        elif choice == "1":
            add_organization()
        elif choice == "2":
            update_organization()
        elif choice == "3":
            delete_organization()
        elif choice == "4":
            view_organizations()

if __name__ == "__main__":
    main()
