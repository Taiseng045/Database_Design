import mysql.connector

# Database connection function
def get_db():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Taiseng@045",
        database="criminal_record_db"
    )
    return conn

# Function to execute SQL from a file
def execute_sql_file(filename):
    conn = get_db()
    cursor = conn.cursor()
    
    # Open the SQL file
    with open(filename, 'r') as file:
        sql = file.read()
        
    # Execute SQL script
    cursor.execute(sql, multi=True)  # multi=True to execute multiple statements
    conn.commit()  # Commit the transaction
    
    conn.close()

# Run the setup when executed
if __name__ == "__main__":
    execute_sql_file('db_setup.sql')  # Run the SQL script from the root directory
    print("Database setup complete!")
