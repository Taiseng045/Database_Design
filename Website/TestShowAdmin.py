# from . import get_db,User
import mysql.connector
DB_NAME = 'criminal_record_db'
def get_db():
    conn = mysql.connector.connect(  # For MySQL
        host="localhost",
        user="root",
        password="Taiseng@045",
        database=DB_NAME
    )
    return conn
def show_admin_user():
    conn = get_db()
    cursor = conn.cursor()

    # Execute the query to show the admin user
    cursor.execute("SELECT * FROM users WHERE role = 'Admin'")

    # Fetch the result
    admin_user = cursor.fetchone()  # Get the first result (if there's only one admin)
    
    if admin_user:
        print("Admin User Details:")
        print(f"ID: {admin_user[0]}")
        print(f"Username: {admin_user[1]}")
        print(f"Password: {admin_user[2]}")  # Note: The password is hashed
        print(f"Role: {admin_user[3]}")
        print(f"Status: {admin_user[4]}")
    else:
        print("No admin user found.")
    
    conn.close()

# Run the function to show the admin user
show_admin_user()