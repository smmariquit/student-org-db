import mariadb
import os
from dotenv import load_dotenv
import data.queries as queries

# Load environment variables
load_dotenv()

# Database connection parameters from the .env file
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_NAME = os.getenv('DB_DATABASE')

def setup_database():
    try:
        # Create database connection
        conn = queries.create_database_connection()
        cursor = conn.cursor()
        
        # Create tables using the function from queries.py
        queries.create_tables(cursor)
        
        conn.commit()
        print("✅ All tables created successfully!")
        
    except mariadb.Error as e:
        print(f"❌ Error setting up database: {e}")
    
    conn.close()
    return cursor

def delete_all_data():
    try:
        # Connect to the database using the function from queries.py
        conn = queries.create_database_connection()
        cursor = conn.cursor()
        
        # Delete data from all tables in reverse order of dependencies
        cursor.execute("DELETE FROM payment")
        cursor.execute("DELETE FROM fee")
        cursor.execute("DELETE FROM committee_role")
        cursor.execute("DELETE FROM committee")
        cursor.execute("DELETE FROM student_role")
        cursor.execute("DELETE FROM member_batch")
        cursor.execute("DELETE FROM joins")
        cursor.execute("DELETE FROM member")
        cursor.execute("DELETE FROM organization")
        
        conn.commit()
        print("✅ All data deleted successfully!")
        
    except mariadb.Error as e:
        print(f"❌ Error deleting data: {e}")

    conn.close()

def load_dummy_data():
    try:
        # Connect to the database using the function from queries.py
        conn = queries.create_database_connection()
        cursor = conn.cursor()
        
        try:
            # Load dummy data using the function from queries.py
            queries.load_dummy_data(cursor)
            conn.commit()
        except mariadb.Error as e:
            print(f"❌ Error loading data: {e}")
            conn.rollback()
        
    except mariadb.Error as e:
        print(f"❌ Error loading data: {e}")
    conn.close()

if __name__ == "__main__":
    cursor = setup_database()
    
    while True:
        print("\n📋 Database Management Options:")
        print("┌────────────────────────────────────────────────────────────")
        print("│ [1] 🗑️  Delete All Data")
        print("│ [2] 📥 Load Organization Data")
        print("│ [0] ↩️  Exit")
        print("└────────────────────────────────────────────────────────────")
        
        choice = input("Enter your choice: ")
        
        if choice == "0":
            break
        elif choice == "1":
            confirm = input("⚠️  Are you sure you want to delete all data? (y/n): ").lower()
            if confirm == "y":
                delete_all_data()
        elif choice == "2":
            queries.load_dummy_data()
        else:
            print("❌ Invalid choice! Please try again.") 