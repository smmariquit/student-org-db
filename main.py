# CMSC 127 ST26L - MySJL
# Final Project - a Python CLI app that simulates a Student Organization Database.
# This is the main file that runs the program.

# This app was created by the following BS Computer Science students at the University of the Philippines Los Baños:
# MARIQUIT, Simonee Ezekiel M.
# CHAN, Liesl Erica
# GERMINAL, Jan Andrew

# TECH STACK: MariaDB, Python
# REFERENCES:
# [1] https://www.geeksforgeeks.org/dunder-magic-methods-python/ - for __init__ and __str__
# [2] https://stackoverflow.com/questions/2491819/how-to-return-a-value-from-init-in-python
# [3] https://docs.pydantic.dev/latest/#pydantic-examples - Pydantic is actually a well-known Python library and in the examples folder, they show how to make a class that models entities. Similar libraries include SQLAlchemy.  
# [4] https://www.geeksforgeeks.org/how-to-use-dotenv-module-in-python/ - for loading environment variables from a .env file.  
# [5] https://mariadb.com/resources/blog/how-to-connect-python-programs-to-mariadb/ - for the MariaDB connector for Python.
# [6] https://asciiflow.com/#/ - We used this really cool ASCII art generator 

import mariadb # Import the official MariaDB connector for Python
import os # Import the OS module to read environment variables, which is necessary for the security of the database connection.
from dotenv import load_dotenv
from src import students, organizations, membership, fees
from src import gui
from data import models, queries

# Load environment variables
load_dotenv()

# Database connection parameters from the .env file
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_NAME = os.getenv('DB_DATABASE')

# Connect to MariaDB
try:
    conn = mariadb.connect(
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=3306,
        database=DB_NAME
    )
    
    # Select the database
    cursor = conn.cursor()
    cursor.execute(f"USE {DB_NAME}")
    
    print("✅ Successfully connected to MariaDB!")

except mariadb.Error as e:
    print(f"❌ Error connecting to MariaDB: {e}")
    exit(1)

# Options to navigate the program 
def print_header():
    print("""┌────────────────────────────────────────────────────────────
│                🎓 Student Organization DB 🎓               """)

def print_menu():
    print("""┌────────────────────────────────────────────────────────────
│ 📋 Main Menu:
├────────────────────────────────────────────────────────────
│ [1] 👥 Manage Students                                     
│ [2] 🏢 Manage Organizations                                
│ [3] 🤝 Manage Memberships                                  
│ [4] 💰 Manage Fees                                         
│ [0] 🚪 Exit                                                
└────────────────────────────────────────────────────────────""")

def print_interface_menu():
    print("""┌────────────────────────────────────────────────────────────
│ 📋 Choose Interface:
├────────────────────────────────────────────────────────────
│ [1] 🖥️  Command Line Interface (CLI)                       
│ [2] 🖼️  Graphical User Interface (GUI)                     
│ [0] 🚪 Exit                                                
└────────────────────────────────────────────────────────────""")

def cli_main():
    while True:
        print_header()
        print_menu()
        
        try:
            choice = input("\n👉 Enter your choice: ")
            
            if choice == "0":
                print("\n👋 Thank you for using the Student Organization Database!")
                break
                
            if choice == "1":
                students.main(conn)
            elif choice == "2":
                organizations.main(conn)
            elif choice == "3":
                membership.main(conn)
            elif choice == "4":
                fees.main(conn)
            else:
                print("❌ Invalid choice! Please try again.")
                
        except ValueError:
            print("❌ Please enter a valid number!")
        except Exception as e:
            print(f"❌ An error occurred: {e}")

def main():
    while True:
        print_header()
        print_interface_menu()
        
        try:
            choice = input("\n👉 Enter your choice: ")
            
            if choice == "0":
                print("\n👋 Thank you for using the Student Organization Database!")
                break
                
            if choice == "1":
                cli_main()
            elif choice == "2":
                gui.main()
            else:
                print("❌ Invalid choice! Please try again.")
                
        except ValueError:
            print("❌ Please enter a valid number!")
        except Exception as e:
            print(f"❌ An error occurred: {e}")

if __name__ == "__main__":
    try:
        main()
    finally:
        # Close database connection
        cursor.close()
        conn.close()
        print("\n🔌 Database connection closed.")

# Proposed CLI Flow
# Some notes: Deleting some things, like for example Organization, may affect the other entities.

# MAIN MENU
# 1. Manage Students
# 2. Manage Organizations
# 3. Manage Memberships
# 4. Manage Fees
# 0. Exit

# 1. Manage Students
#     1. Add Student
#         → Input: Student Number, Name, Gender, Degree Program, Batch
#     2. Update Student
#         → Input: Select Student by ID
#           1. Update Student Number
#               → Input: New Student Number
#           2. Update Name
#               → Input: First and Last Name
#           3. Update Gender
#               → Input: M or F
#           4. Update Degree Program
#               → Input: Valid degree program name/code
#           5. Update Batch
#               → Input: Year (e.g. 2022)
#           0. Back
#     3. Delete Student
#         → Input: Confirm deletion
#     4. View Students
#           1. Print All Students
#           2. Find Student by ID
#               → Input: Student ID
#           3. Filter by Organization
#               → Input: Organization name or ID
#           4. Filter by Batch
#               → Input: Year (e.g. 2021)
#           0. Back
#     0. Back

# 2. Manage Organizations
#     1. Add Organization
#         → Input: Org Name, Type, Description
#     2. Update Organization
#         → Input: Select Organization by ID
#     3. Delete Organization  # WARNING: This will also affect all associated memberships and fee records! D:
#         → Input: Confirm deletion (Y/N)
#     4. View Organizations
#           1. View All Organizations
#           2. View by Type
#               → Input: Org Type
#           0. Back
#     0. Back

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
# 4. Manage Fees
#     → Input: Select Organization by ID
#     1. Add Fee
#         → Input: Member ID, Amount, Due Date (YYYY-MM-DD), Semester, Academic Year
#     2. Update Fee
#         → Input: Select Fee Record
#     3. Delete Fee
#         → Input: Confirm deletion (Y/N)
#     4. Generate Financial Status
#         → Input: Semester, Academic Year
#     5. View Fee Reports
#         1. Members with Unpaid Dues for Given Semester (Report #2)
#           → Input: Semester, Academic Year
#         2. A Member's Unpaid Dues Across All Orgs (Report #3)
#           → Input: Student ID
#         3. Late Payments in Given Semester (Report #6)
#           → Input: Semester, Academic Year
#         4. Total Paid and Unpaid Fees as of Date (Report #9)
#           → Input: Date (YYYY-MM-DD)
#         0. Back
#     0. Back
# 0. Back