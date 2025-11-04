import mysql.connector

# Function to connect to MySQL
def connect_db():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="bank",
            auth_plugin="mysql_native_password"  # ensures compatibility
        )
        return conn
    except mysql.connector.Error as err:
        print("❌ Database connection failed!")
        print("Reason:", err)
        return None


# Function to add a new account
def add_account():
    conn = connect_db()
    if conn:
        cur = conn.cursor()
        name = input("Enter Account Holder Name: ")
        city = input("Enter City: ")
        contact = input("Enter Contact Number: ")
        balance = float(input("Enter Initial Balance: "))
        query = "INSERT INTO accounts (name, city, contact, balance) VALUES (%s, %s, %s, %s)"
        cur.execute(query, (name, city, contact, balance))
        conn.commit()
        print("✅ Account created successfully!")
        conn.close()


# Function to view all accounts
def view_all_accounts():
    conn = connect_db()
    if conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM accounts")
        rows = cur.fetchall()
        print("\n🏦 BANK ACCOUNTS:")
        print("-" * 60)
        for r in rows:
            print(f"Acc No: {r[0]}, Name: {r[1]}, City: {r[2]}, Contact: {r[3]}, Balance: ₹{r[4]:.2f}")
        print("-" * 60)
        conn.close()


# Function to deposit money
def deposit_money():
    conn = connect_db()
    if conn:
        cur = conn.cursor()
        acc_no = int(input("Enter Account Number: "))
        amount = float(input("Enter Amount to Deposit: "))
        cur.execute("UPDATE accounts SET balance = balance + %s WHERE acc_no = %s", (amount, acc_no))
        conn.commit()
        if cur.rowcount > 0:
            print("💰 Deposit Successful!")
        else:
            print("❌ Invalid Account Number!")
        conn.close()


# Function to withdraw money
def withdraw_money():
    conn = connect_db()
    if conn:
        cur = conn.cursor()
        acc_no = int(input("Enter Account Number: "))
        amount = float(input("Enter Amount to Withdraw: "))
        cur.execute("SELECT balance FROM accounts WHERE acc_no = %s", (acc_no,))
        record = cur.fetchone()
        if record:
            if record[0] >= amount:
                cur.execute("UPDATE accounts SET balance = balance - %s WHERE acc_no = %s", (amount, acc_no))
                conn.commit()
                print("💸 Withdrawal Successful!")
            else:
                print("⚠️ Insufficient Balance!")
        else:
            print("❌ Account Not Found!")
        conn.close()


# Function to delete an account
def delete_account():
    conn = connect_db()
    if conn:
        cur = conn.cursor()
        acc_no = int(input("Enter Account Number to Delete: "))
        cur.execute("DELETE FROM accounts WHERE acc_no = %s", (acc_no,))
        conn.commit()
        if cur.rowcount > 0:
            print("🗑️ Account Deleted Successfully!")
        else:
            print("❌ Account Not Found!")
        conn.close()


# Main menu
def main_menu():
    while True:
        print("""
========= BANK MANAGEMENT SYSTEM =========
1. Add New Account
2. View All Accounts
3. Deposit Money
4. Withdraw Money
5. Delete Account
6. Exit
==========================================
""")
        choice = input("Enter your choice (1-6): ")

        if choice == '1':
            add_account()
        elif choice == '2':
            view_all_accounts()
        elif choice == '3':
            deposit_money()
        elif choice == '4':
            withdraw_money()
        elif choice == '5':
            delete_account()
        elif choice == '6':
            print("👋 Thank you for using Bank Management System!")
            break
        else:
            print("❌ Invalid choice! Please try again.\n")


# Run program
if __name__ == "__main__":
    main_menu()
