import mariadb
import os
from dotenv import load_dotenv
from data import queries
from data.models import student, organization, fee, committee
from src import fees, organizations, students

# does not yet use mysql

try:
    conn = mariadb.connect(
        user=organizationer,
        password=uplbsqlsociety,
        host=localhost,
        port=3306,
        database=organization
    )
    
    print("Successfully connected to MariaDB!")
   
except mariadb.Error as e:
    print(f"Error connecting to MariaDB: {e}")
   
cursor = conn.cursor()

# Main menu
while True:
    print("---------------[ Student Org Database ]---------------")
    print("[1] Manage Students")
    print("[2] Manage Membership")
    print("[3] Manage Organizations")
    print("[4] Manage Fees")
    print("[4] Exit ")
    
    choice = int(input())

# Proposed CLI Fllow
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
#     3. Delete Organization  # WARNING: This will also affect all associated memberships and fee records!
#         → Input: Confirm deletion (Y/N)
#     4. View Organizations
#           1. View All Organizations
#           2. View by Type
#               → Input: Org Type (e.g. Academic, Varsitarian, etc.)
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
#         2. A Member’s Unpaid Dues Across All Orgs (Report #3)
#           → Input: Student ID
#         3. Late Payments in Given Semester (Report #6)
#           → Input: Semester, Academic Year
#         4. Total Paid and Unpaid Fees as of Date (Report #9)
#           → Input: Date (YYYY-MM-DD)
#         0. Back
#     0. Back
# 0. Back