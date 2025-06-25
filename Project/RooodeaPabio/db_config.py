import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root2",
        password="root2",
        database="employee_db",
        auth_plugin="mysql_native_password"
    )
