import employee_model

def initialize():
    employee_model.create_table()

def add(emp_id, name, age, department, salary, contact):
    employee_model.add_employee(emp_id, name, age, department, salary, contact)

def view_all():
    return employee_model.get_all_employees()

def update(emp_id, name, age, department, salary, contact):
    employee_model.update_employee(emp_id, name, age, department, salary, contact)

def delete(emp_id):
    employee_model.delete_employee(emp_id)
