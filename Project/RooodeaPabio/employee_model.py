import mysql.connector
from db_config import get_connection

def create_table():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS employees (
            id VARCHAR(10) PRIMARY KEY,
            name VARCHAR(100),
            age INT,
            department VARCHAR(100),
            salary DECIMAL(10,2),
            contact VARCHAR(20)
        )
    """)
    conn.commit()
    conn.close()

def add_employee(emp_id, name, age, department, salary, contact):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO employees (id, name, age, department, salary, contact) VALUES (%s, %s, %s, %s, %s, %s)",
                   (emp_id, name, age, department, salary, contact))
    conn.commit()
    conn.close()

def get_all_employees():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM employees")
    rows = cursor.fetchall()
    conn.close()
    return rows

def update_employee(emp_id, name, age, department, salary, contact):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE employees SET name=%s, age=%s, department=%s, salary=%s, contact=%s WHERE id=%s",
                   (name, age, department, salary, contact, emp_id))
    conn.commit()
    conn.close()

def delete_employee(emp_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM employees WHERE id=%s", (emp_id,))
    conn.commit()
    conn.close()
