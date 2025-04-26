import mariadb
import os
from dotenv import load_dotenv
from data import queries
from data.models import student, organization, fee, committee

try:
    conn = mariadb.connect(
        user=USER
        password=PASSWORD
        host=HOST
        port=PORT
        database=DATABASE
    )
    
    print("Successfully connected to MariaDB!")
   
except mariadb.Error as e:
    print(f"Error connecting to MariaDB: {e}")
   
cursor = conn.cursor()

