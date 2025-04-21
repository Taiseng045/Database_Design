from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager, UserMixin
import mysql.connector

# db = SQLAlchemy()
DB_NAME = "criminal_record_db"
def get_db():
    conn = mysql.connector.connect(  # For MySQL
        host="localhost",
        user="root",
        password="password",   # input your Sql password
        database=DB_NAME
    )
    return conn
def local_con():
    conn = mysql.connector.connect(  # For MySQL
        host="localhost",
        user="root",
        password="password",   # input your Sql password
    )
    return conn
def execute_sql_file(filename):
    conn = local_con()
    cursor = conn.cursor()

    # Open the SQL file and execute its content
    with open(filename, 'r') as file:
        sql = file.read()
    sql_statements = sql.split(';')
    # Remove any empty statements from the list
    sql_statements = [stmt.strip() for stmt in sql_statements if stmt.strip()]
    # Execute the SQL script
    try:
        for statement in sql_statements:
            cursor.execute(statement) # multi=True allows executing multiple statements
        conn.commit()  # Commit the transaction
    except mysql.connector.Error as err:
        print(f"Error executing SQL: {err}")
    finally:
        cursor.close()
        conn.close()
def create_database(app):
    # Check if the database exists and if not, create it
    with app.app_context():
        print("Setting up the database...")
        execute_sql_file('Website/db_setup.sql')  # Make sure this path is correct relative to __init__.py
        print("Database setup complete!")
    conn = get_db()
    cursor = conn.cursor()
    with open('Website/AdminCreation.sql', 'r') as file:
        sql = file.read()
    cursor.execute(sql)  # multi=True allows executing multiple statements
    conn.commit()
    conn.close()
    print("Admin creation is completed!")
class User(UserMixin):
    def __init__(self, id, name, username, password, role, status, description, delete_at, created_at, updated_at):
        self.id = id
        self.name = name
        self.username = username
        self.password = password
        self.role = role
        self.status = status
        self.description = description
        self.delete_at = delete_at
        self.created_at = created_at
        self.updated_at = updated_at
def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'DSKFAJSF'
    from .view import views
    from .auth import auth
    
    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")

    # from .models import User
    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    @login_manager.user_loader
    def load_user(id):
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE id = %s", (id,))
        user_data = cursor.fetchone()
        conn.close()
        if user_data:
            user = User(*user_data)
            return user
        return None
    return app

