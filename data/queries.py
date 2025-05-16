import mariadb
import sys
from tabulate import tabulate  # For pretty printing tables
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database connection parameters from the .env file

# Connect to MariaDB
def create_database_connection():
    DB_USER = os.getenv('DB_USER')
    DB_PASSWORD = os.getenv('DB_PASSWORD')
    DB_HOST = os.getenv('DB_HOST')
    
    try:
        # First connect without database selection
        conn = mariadb.connect(
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=3306
        )
        cursor = conn.cursor()
        
        # Create database if it doesn't exist
        cursor.execute("CREATE DATABASE IF NOT EXISTS organization")
        cursor.close()
        conn.close()
        
        # Now connect with database selected
        conn = mariadb.connect(
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=3306,
            database="organization"
        )
        return conn
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB: {e}")
        sys.exit(1)

def create_tables(cursor):
    # Create organization table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS organization (
            `Organization ID` int NOT NULL,
            `Organization Name` varchar(128),
            CONSTRAINT PK_Organization PRIMARY KEY (`Organization ID`)
        )
    """)

    # Create member table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS member (
            `Student Number` varchar(128) NOT NULL,
            `First Name` varchar(128) NOT NULL,
            `Middle Name` varchar(128),
            `Last Name` varchar(128) NOT NULL,
            `Gender` varchar(128),
            `Degree Program` varchar(128),
            CONSTRAINT PK_Member PRIMARY KEY (`Student Number`)
        )
    """)

    # Create joins table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS joins (
            `Student Number` varchar(128) NOT NULL,
            `Organization ID` int NOT NULL,
            `Academic Year` varchar(128) NOT NULL,
            `Semester` varchar(128) NOT NULL,
            `Member Role` varchar(128) NOT NULL,
            `Member Status` varchar(128) NOT NULL,
            CONSTRAINT PK_Joins PRIMARY KEY (`Student Number`, `Organization ID`, `Academic Year`, `Semester`),
            CONSTRAINT UQ_SN UNIQUE (`Student Number`)
        )
    """)

    # Create member_batch table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS member_batch (
            `Student Number` varchar(128) NOT NULL,
            `Organization ID` int NOT NULL,
            `Batch` int NOT NULL,
            CONSTRAINT PK_Joins PRIMARY KEY(`Student Number`, `Organization ID`, `Batch`)
        )
    """)

    # Create student_role table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS student_role (
            `Student Number` varchar(128) NOT NULL,
            `Organization ID` int NOT NULL,
            `Committee Name` varchar(128) NOT NULL,
            `Role` varchar(128) NOT NULL,
            CONSTRAINT PK_Joins PRIMARY KEY(`Student Number`, `Organization ID`, `Committee Name`)
        )
    """)

    # Create committee table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS committee (
            `Committee Name` varchar(128) NOT NULL,
            `Organization ID` int NOT NULL,
            `Semester` varchar(128) NOT NULL,
            `Academic Year` varchar(128) NOT NULL,
            CONSTRAINT PK_Committee PRIMARY KEY(`Committee Name`, `Organization ID`)
        )
    """)

    # Create committee_role table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS committee_role (
            `Committee Name` varchar(128) NOT NULL,
            `Organization ID` int NOT NULL,
            `Role` varchar(128) NOT NULL,
            CONSTRAINT PK_CommitteeRole PRIMARY KEY(`Committee Name`, `Organization ID`, `Role`)
        )
    """)

    # Create fee table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS fee (
            `Organization ID` int NOT NULL,
            `Student Number` varchar(128) NOT NULL,
            `Fee Name` varchar(128) NOT NULL,
            `Due Date` date NOT NULL,
            `Academic Year` varchar(128) NOT NULL,
            `Status` varchar(128) NOT NULL,
            `Semester` varchar(128) NOT NULL,
            `Amount` varchar(128) NOT NULL,
            CONSTRAINT PK_Fee PRIMARY KEY(`Fee Name`, `Student Number`, `Organization ID`, `Academic Year`, `Semester`)
        )
    """)

    # Create payment table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS payment (
            `Fee Name` varchar(128) NOT NULL,
            `Student Number` varchar(128) NOT NULL,
            `Organization ID` int NOT NULL,
            `Full Payment Date` date NOT NULL,
            `Due Date` date NOT NULL,
            `Payment Late?` boolean NOT NULL,
            CONSTRAINT PK_Payment PRIMARY KEY(`Fee Name`, `Student Number`, `Organization ID`, `Full Payment Date`)
        )
    """)

def load_dummy_data():
    try:
        # Create our own connection
        conn = create_database_connection()
        cursor = conn.cursor()
        
        # Organization data
        org_insert = """
        INSERT INTO organization(`Organization ID`, `Organization Name`) VALUES 
        ('11111111', 'Malayang Asosasyon ng Shih Tzu at Siberian Husky'),
        ('22222222', 'Circle of Secretive Species'),
        ('33333333', 'Alliance of Cat Students for Science'),
        ('44444444', 'Young Squirrel Entrepreneurial Society'),
        ('55555555', 'Cats, Penguins, and Sloths Triad')
        """
        
        # Member data
        member_insert = """
        INSERT INTO member(`Student Number`, `First Name`, `Middle Name`, `Last Name`, `Gender`, `Degree Program`) VALUES
        ('20230001', 'Luna', 'B.', 'Meowington', 'Female', 'BS Zoology'),
        ('20230002', 'Barkley', NULL, 'Howlson', 'Male', 'BS Computer Science'),
        ('20230003', 'Otto', 'J.', 'Riverpaw', 'Male', 'BS Environmental Science'),
        ('20230004', 'Gerry', 'K.', 'Neckson', 'Nonbinary', 'BS Architecture'),
        ('20230005', 'Tina', 'M.', 'Shellford', 'Female', 'BS Marine Biology')
        """
        
        # Joins data
        joins_insert = """
        INSERT INTO joins(`Student Number`, `Organization ID`, `Academic Year`, `Semester`, `Member Role`, `Member Status`) VALUES
        ('20230001', 11111111, '2024-2025', '1st', 'President', 'Active'),
        ('20230002', 22222222, '2024-2025', '1st', 'Treasurer', 'Active'),
        ('20230003', 33333333, '2024-2025', '2nd', 'Member', 'Inactive'),
        ('20230004', 44444444, '2024-2025', '1st', 'Secretary', 'Active'),
        ('20230005', 55555555, '2024-2025', '1st', 'Member', 'Probation')
        """
        
        # Member batch data
        batch_insert = """
        INSERT INTO member_batch(`Student Number`, `Organization ID`, `Batch`) VALUES
        ('20230001', 11111111, 2023),
        ('20230002', 22222222, 2022),
        ('20230003', 33333333, 2021),
        ('20230004', 44444444, 2023),
        ('20230005', 55555555, 2024)
        """
        
        # Student role data
        role_insert = """
        INSERT INTO student_role(`Student Number`, `Organization ID`, `Committee Name`, `Role`) VALUES
        ('20230001', 11111111, 'Snack Patrol', 'Snackmaster'),
        ('20230002', 22222222, 'Fundraising Ferrets', 'Finance Head'),
        ('20230003', 33333333, 'Otter Awareness', 'Public Relations'),
        ('20230004', 44444444, 'Tall Talks', 'Moderator'),
        ('20230005', 55555555, 'Shell Squad', 'Logistics')
        """
        
        # Committee data
        committee_insert = """
        INSERT INTO committee(`Committee Name`, `Organization ID`, `Semester`, `Academic Year`) VALUES
        ('Snack Patrol', 11111111, '1st', '2024-2025'),
        ('Fundraising Ferrets', 22222222, '1st', '2024-2025'),
        ('Otter Awareness', 33333333, '2nd', '2024-2025'),
        ('Tall Talks', 44444444, '1st', '2024-2025'),
        ('Shell Squad', 55555555, '1st', '2024-2025')
        """
        
        # Committee role data
        committee_role_insert = """
        INSERT INTO committee_role(`Committee Name`, `Organization ID`, `Role`) VALUES
        ('Snack Patrol', 11111111, 'Snackmaster'),
        ('Fundraising Ferrets', 22222222, 'Finance Head'),
        ('Otter Awareness', 33333333, 'Public Relations'),
        ('Tall Talks', 44444444, 'Moderator'),
        ('Shell Squad', 55555555, 'Logistics')
        """
        
        # Fee data
        fee_insert = """
        INSERT INTO fee(`Organization ID`, `Student Number`, `Fee Name`, `Due Date`, `Academic Year`, `Status`, `Semester`, `Amount`) VALUES
        (11111111, '20230001', 'Annual Dues', '2024-10-01', '2024-2025', 'Pending', '1st', '300'),
        (22222222, '20230002', 'Event Fee', '2024-09-15', '2024-2025', 'Paid', '1st', '150'),
        (33333333, '20230003', 'Otter Field Trip', '2025-01-10', '2024-2025', 'Unpaid', '2nd', '500'),
        (44444444, '20230004', 'Poster Printing', '2024-11-05', '2024-2025', 'Paid', '1st', '100'),
        (55555555, '20230005', 'Turtle Shell Care', '2024-12-12', '2024-2025', 'Pending', '1st', '250')
        """
        
        # Payment data
        payment_insert = """
        INSERT INTO payment(`Fee Name`, `Student Number`, `Organization ID`, `Full Payment Date`, `Due Date`, `Payment Late?`) VALUES
        ('Annual Dues', '20230001', 11111111, '2024-10-02', '2024-10-01', TRUE),
        ('Event Fee', '20230002', 22222222, '2024-09-10', '2024-09-15', FALSE),
        ('Otter Field Trip', '20230003', 33333333, '2025-01-15', '2025-01-10', TRUE),
        ('Poster Printing', '20230004', 44444444, '2024-11-04', '2024-11-05', FALSE),
        ('Turtle Shell Care', '20230005', 55555555, '2024-12-10', '2024-12-12', FALSE)
        """
        
        try:
            cursor.execute(org_insert)
            cursor.execute(member_insert)
            cursor.execute(joins_insert)
            cursor.execute(batch_insert)
            cursor.execute(role_insert)
            cursor.execute(committee_insert)
            cursor.execute(committee_role_insert)
            cursor.execute(fee_insert)
            cursor.execute(payment_insert)
            conn.commit()
            print("✅ Dummy data loaded successfully!")
        except mariadb.Error as e:
            print(f"❌ Error loading dummy data: {e}")
            conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()
            
    except mariadb.Error as e:
        print(f"❌ Error connecting to database: {e}")
        raise e

def main():
    # Create database connection
    conn = create_database_connection()
    cursor = conn.cursor()

    # Create database if not exists
    cursor.execute("CREATE DATABASE IF NOT EXISTS organization")
    cursor.execute("USE organization")

    # Create tables
    create_tables(cursor)

    # Commit changes and close connection
    conn.commit()
    conn.close()

if __name__ == "__main__":
    main()

def create_student(cursor, student_number, first_name, middle_name, last_name, gender, degree_program):
    query = """
        INSERT INTO member (`Student Number`, `First Name`, `Middle Name`, `Last Name`, `Gender`, `Degree Program`)
        VALUES (?, ?, ?, ?, ?, ?)
    """
    cursor.execute(query, (student_number, first_name, middle_name, last_name, gender, degree_program))

def get_student_by_id(cursor, student_number):
    query = "SELECT * FROM member WHERE `Student Number` = ?"
    cursor.execute(query, (student_number,))
    return cursor.fetchone()

def get_organization_members(organization_id):
    try:
        conn = create_database_connection()
        cursor = conn.cursor()
        
        query = """
        SELECT 
            m.`Student Number` as student_number,
            m.`Last Name` as last_name,
            m.`First Name` as first_name,
            sr.`Role` as role,
            j.`Member Status` as status,
            m.`Gender` as gender,
            m.`Degree Program` as degree_program,
            mb.`Batch` as batch,
            sr.`Committee Name` as committee
        FROM member m
        JOIN member_batch mb 
            ON m.`Student Number` = mb.`Student Number` 
        JOIN student_role sr 
            ON m.`Student Number` = sr.`Student Number`
            AND mb.`Organization ID` = sr.`Organization ID`
        JOIN joins j 
            ON m.`Student Number` = j.`Student Number`
            AND j.`Organization ID` = sr.`Organization ID`
        WHERE sr.`Organization ID` = %s
        """
        
        cursor.execute(query, (organization_id,))
        results = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        return results
        
    except mariadb.Error as e:
        print(f"Error executing query: {e}")
        return []

def get_unpaid_fees_by_organization(organization_id, academic_year, semester):
    try:
        conn = create_database_connection()
        cursor = conn.cursor()
        
        query = """
        SELECT 
            f.`Organization ID` as organization_id,
            m.`Student Number` as student_number,
            m.`Last Name` as last_name,
            m.`First Name` as first_name,
            f.`Fee Name` as fee_name,
            f.`Amount` as amount,
            f.`Due Date` as due_date,
            f.`Status` as status
        FROM member m
        JOIN fee f ON m.`Student Number` = f.`Student Number`
        WHERE f.`Status` = 'Unpaid'
        AND f.`Organization ID` = %s
        AND f.`Academic Year` = %s
        AND f.`Semester` = %s
        """
        
        cursor.execute(query, (organization_id, academic_year, semester))
        results = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        return results
        
    except mariadb.Error as e:
        print(f"Error executing query: {e}")
        return []

def print_members_table(members):
    if not members:
        print("No members found.")
        return

    headers = ["Student Number", "Last Name", "First Name", "Role", "Status", "Gender", "Degree Program", "Batch", "Committee"]
    print(tabulate(members, headers=headers, tablefmt="grid"))

def print_unpaid_fees_table(fees):
    if not fees:
        print("No unpaid fees found.")
        return

    headers = ["Organization ID", "Student Number", "Last Name", "First Name", "Fee Name", "Amount", "Due Date", "Status"]
    print(tabulate(fees, headers=headers, tablefmt="grid"))
