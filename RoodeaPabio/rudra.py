import mysql.connector

# Database connection function
def connect_db():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            auth_plugin='mysql_native_password'
        )

        cur = conn.cursor()
        cur.execute("CREATE DATABASE IF NOT EXISTS employee")
        cur.execute("USE employee")

        # Create table if not exists
        cur.execute("""
            CREATE TABLE IF NOT EXISTS employee (
                emp_id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(50),
                city VARCHAR(50),
                contact VARCHAR(15),
                salary DECIMAL(10,2),
                department VARCHAR(50)
            )
        """)
        conn.commit()
        return conn

    except mysql.connector.Error as e:
        print("❌ Error connecting to MySQL:", e)
        return None


# Add a new employee
def add_employee():
    conn = connect_db()
    if conn:
        cur = conn.cursor()
        name = input("Enter employee name: ")
        city = input("Enter city: ")
        contact = input("Enter contact number: ")
        salary = float(input("Enter salary: "))
        department = input("Enter department: ")

        query = "INSERT INTO employee (name, city, contact, salary, department) VALUES (%s, %s, %s, %s, %s)"
        cur.execute(query, (name, city, contact, salary, department))
        conn.commit()
        print("✅ Employee added successfully!\n")
        conn.close()


# View all employees
def view_all():
    conn = connect_db()
    if conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM employee")
        rows = cur.fetchall()

        print("\n📋 EMPLOYEE DETAILS:")
        print("="*70)
        for row in rows:
            print(f"ID: {row[0]}, Name: {row[1]}, City: {row[2]}, Contact: {row[3]}, Salary: {row[4]}, Dept: {row[5]}")
        print("="*70)
        conn.close()


# Update employee salary
def update_salary():
    conn = connect_db()
    if conn:
        cur = conn.cursor()
        emp_id = int(input("Enter Employee ID to update salary: "))
        new_salary = float(input("Enter new salary: "))

        cur.execute("UPDATE employee SET salary=%s WHERE emp_id=%s", (new_salary, emp_id))
        conn.commit()
        print("✅ Salary updated successfully!\n")
        conn.close()


# Delete an employee
def delete_employee():
    conn = connect_db()
    if conn:
        cur = conn.cursor()
        emp_id = int(input("Enter Employee ID to delete: "))
        cur.execute("DELETE FROM employee WHERE emp_id=%s", (emp_id,))
        conn.commit()
        print("🗑️ Employee deleted successfully!\n")
        conn.close()


# Main menu
def main_menu():
    while True:
        print("""
========= EMPLOYEE MANAGEMENT SYSTEM =========
1. Add Employee
2. View All Employees
3. Update Salary
4. Delete Employee
5. Exit
==============================================
        """)
        choice = input("Enter your choice: ")

        if choice == '1':
            add_employee()
        elif choice == '2':
            view_all()
        elif choice == '3':
            update_salary()
        elif choice == '4':
            delete_employee()
        elif choice == '5':
            print("👋 Exiting... Goodbye!")
            break
        else:
            print("❌ Invalid choice! Please try again.\n")


# Run program
if __name__ == "__main__":
    main_menu()
