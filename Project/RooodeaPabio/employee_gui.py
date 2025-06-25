import tkinter as tk
from tkinter import messagebox, ttk
import employee_controller as ctrl

class SmartEntry(tk.Entry):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bind('<Control-BackSpace>', self.ctrl_backspace)

    def ctrl_backspace(self, event):
        index = self.index(tk.INSERT)
        if index == 0:
            return "break"
        text = self.get()
        while index > 0 and text[index - 1] == ' ':
            index -= 1
        while index > 0 and text[index - 1] not in (' ', '\t'):
            index -= 1
        self.delete(index, tk.INSERT)
        return "break"

def refresh_table(tree, sort_by=None, descending=False):
    data = ctrl.view_all()
    if sort_by:
        col_index = {"ID": 0, "Name": 1, "Age": 2, "Department": 3, "Salary": 4, "Contact": 5}[sort_by]
        data.sort(key=lambda x: str(x[col_index]), reverse=descending)
    for row in tree.get_children():
        tree.delete(row)
    for emp in data:
        tree.insert("", "end", values=emp)

def gui():
    root = tk.Tk()
    root.title("Employee Management System")
    root.geometry("880x550")
    root.configure(bg="#f5f5f5")

    tk.Label(root, text="Employee ID", bg="#f5f5f5").grid(row=0, column=0, padx=5, pady=5, sticky='w')
    id_entry = SmartEntry(root)
    id_entry.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(root, text="Name", bg="#f5f5f5").grid(row=1, column=0, padx=5, pady=5, sticky='w')
    name_entry = SmartEntry(root)
    name_entry.grid(row=1, column=1, padx=5, pady=5)

    tk.Label(root, text="Age", bg="#f5f5f5").grid(row=2, column=0, padx=5, pady=5, sticky='w')
    age_entry = SmartEntry(root)
    age_entry.grid(row=2, column=1, padx=5, pady=5)

    tk.Label(root, text="Department", bg="#f5f5f5").grid(row=3, column=0, padx=5, pady=5, sticky='w')
    dept_entry = SmartEntry(root)
    dept_entry.grid(row=3, column=1, padx=5, pady=5)

    tk.Label(root, text="Salary", bg="#f5f5f5").grid(row=4, column=0, padx=5, pady=5, sticky='w')
    salary_entry = SmartEntry(root)
    salary_entry.grid(row=4, column=1, padx=5, pady=5)

    tk.Label(root, text="Contact", bg="#f5f5f5").grid(row=5, column=0, padx=5, pady=5, sticky='w')
    contact_entry = SmartEntry(root)
    contact_entry.grid(row=5, column=1, padx=5, pady=5)

    def add_emp():
        try:
            emp_id = id_entry.get().strip()
            name = name_entry.get()
            age = int(age_entry.get())
            dept = dept_entry.get()
            salary = float(salary_entry.get())
            contact = contact_entry.get()
            if not emp_id:
                messagebox.showerror("Error", "Employee ID is required")
                return
            ctrl.add(emp_id, name, age, dept, salary, contact)
            refresh_table(tree)
            for entry in [id_entry, name_entry, age_entry, dept_entry, salary_entry, contact_entry]:
                entry.delete(0, tk.END)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def update_emp():
        selected = tree.focus()
        if not selected:
            messagebox.showinfo("Select", "Select a row to update")
            return
        values = tree.item(selected, "values")
        try:
            emp_id = values[0]
            ctrl.update(emp_id, name_entry.get(), int(age_entry.get()), dept_entry.get(), float(salary_entry.get()), contact_entry.get())
            refresh_table(tree)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def delete_emp():
        selected = tree.focus()
        if not selected:
            messagebox.showinfo("Select", "Select a row to delete")
            return
        emp_id = tree.item(selected, "values")[0]
        ctrl.delete(emp_id)
        refresh_table(tree)

    def on_select(event):
        selected = tree.focus()
        if selected:
            values = tree.item(selected, "values")
            id_entry.delete(0, tk.END)
            id_entry.insert(0, values[0])
            name_entry.delete(0, tk.END)
            name_entry.insert(0, values[1])
            age_entry.delete(0, tk.END)
            age_entry.insert(0, values[2])
            dept_entry.delete(0, tk.END)
            dept_entry.insert(0, values[3])
            salary_entry.delete(0, tk.END)
            salary_entry.insert(0, values[4])
            contact_entry.delete(0, tk.END)
            contact_entry.insert(0, values[5])

    tk.Button(root, text="Add", width=10, bg="#d4fcd6", command=add_emp).grid(row=6, column=0, padx=5, pady=10)
    tk.Button(root, text="Update", width=10, bg="#ffe9b3", command=update_emp).grid(row=6, column=1, padx=5, pady=10)
    tk.Button(root, text="Delete", width=10, bg="#ffc9c9", command=delete_emp).grid(row=6, column=2, padx=5, pady=10)

    cols = ("ID", "Name", "Age", "Department", "Salary", "Contact")
    tree = ttk.Treeview(root, columns=cols, show="headings")
    for col in cols:
        tree.heading(col, text=col, command=lambda _col=col: sort_column(_col))
        tree.column(col, width=130)
    tree.grid(row=7, column=0, columnspan=4, padx=10, pady=20)
    tree.bind("<<TreeviewSelect>>", on_select)

    sort_states = {col: False for col in cols}
    def sort_column(col):
        sort_states[col] = not sort_states[col]
        refresh_table(tree, sort_by=col, descending=sort_states[col])

    style = ttk.Style()
    style.theme_use("default")
    style.configure("Treeview", background="#ffffff", foreground="black", fieldbackground="#ffffff", rowheight=25)
    style.map("Treeview", background=[("selected", "#c0ddff")])

    refresh_table(tree)
    root.mainloop()
