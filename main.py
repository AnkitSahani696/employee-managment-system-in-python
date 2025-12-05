import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from mysql.connector import Error
import hashlib
import time

# Database Configuration
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Ankit@1234',  # Apna MySQL password yahan dale
    'database': 'employee_db'
}


# Database Connection Function
def get_db_connection():
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        return connection
    except Error as e:
        messagebox.showerror("Database Error", f"Error: {e}")
        return None


# Database Setup
def setup_database():
    try:
        conn = mysql.connector.connect(
            host=DB_CONFIG['host'],
            user=DB_CONFIG['user'],
            password=DB_CONFIG['password']
        )
        cursor = conn.cursor()

        # Create database
        cursor.execute("CREATE DATABASE IF NOT EXISTS employee_db")
        cursor.execute("USE employee_db")

        # Create users table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(50) UNIQUE NOT NULL,
                password VARCHAR(255) NOT NULL,
                email VARCHAR(100),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Create employees table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS employees (
                emp_id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                email VARCHAR(100),
                phone VARCHAR(15),
                department VARCHAR(50),
                position VARCHAR(50),
                salary DECIMAL(10, 2),
                join_date DATE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        conn.commit()
        cursor.close()
        conn.close()
    except Error as e:
        print(f"Database setup error: {e}")


# Hash password
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


# Splash Screen
class SplashScreen:
    def __init__(self, root):
        self.root = root
        self.root.title("Employee Management System")
        self.root.geometry("600x400")
        self.root.resizable(False, False)

        # Center window
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - 600) // 2
        y = (screen_height - 400) // 2
        self.root.geometry(f"600x400+{x}+{y}")

        # Background
        self.canvas = tk.Canvas(root, width=600, height=400, bg="#1e3a8a")
        self.canvas.pack()

        # Title
        self.canvas.create_text(300, 150, text="Employee Management System",
                                font=("Arial", 28, "bold"), fill="white")

        # Subtitle
        self.canvas.create_text(300, 200, text="Loading...",
                                font=("Arial", 14), fill="#93c5fd")

        # Progress bar
        self.progress = ttk.Progressbar(root, length=400, mode='determinate')
        self.canvas.create_window(300, 280, window=self.progress)

        # Version
        self.canvas.create_text(300, 350, text="Version 1.0",
                                font=("Arial", 10), fill="#60a5fa")

        self.load()

    def load(self):
        for i in range(101):
            self.progress['value'] = i
            self.root.update_idletasks()
            time.sleep(0.02)

        self.root.destroy()
        open_login()


# Login Page
class LoginPage:
    def __init__(self, root):
        self.root = root
        self.root.title("Login - Employee Management System")
        self.root.geometry("400x500")
        self.root.resizable(False, False)
        self.root.configure(bg="#f0f9ff")

        # Center window
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - 400) // 2
        y = (screen_height - 500) // 2
        self.root.geometry(f"400x500+{x}+{y}")

        # Header
        header_frame = tk.Frame(root, bg="#1e40af", height=100)
        header_frame.pack(fill="x")

        tk.Label(header_frame, text="Login", font=("Arial", 24, "bold"),
                 bg="#1e40af", fg="white").pack(pady=30)

        # Main frame
        main_frame = tk.Frame(root, bg="#f0f9ff")
        main_frame.pack(pady=40)

        # Username
        tk.Label(main_frame, text="Username:", font=("Arial", 12),
                 bg="#f0f9ff").pack(anchor="w", pady=(10, 5))
        self.username_entry = tk.Entry(main_frame, font=("Arial", 12), width=30)
        self.username_entry.pack(pady=(0, 20))

        # Password
        tk.Label(main_frame, text="Password:", font=("Arial", 12),
                 bg="#f0f9ff").pack(anchor="w", pady=(10, 5))
        self.password_entry = tk.Entry(main_frame, font=("Arial", 12),
                                       width=30, show="*")
        self.password_entry.pack(pady=(0, 20))

        # Login button
        tk.Button(main_frame, text="Login", font=("Arial", 14, "bold"),
                  bg="#1e40af", fg="white", width=20, command=self.login).pack(pady=20)

        # Register link
        tk.Label(main_frame, text="Don't have an account?",
                 font=("Arial", 10), bg="#f0f9ff").pack()
        tk.Button(main_frame, text="Register Here", font=("Arial", 10, "underline"),
                  bg="#f0f9ff", fg="#1e40af", border=0,
                  command=self.open_register).pack()

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if not username or not password:
            messagebox.showerror("Error", "Please fill all fields")
            return

        conn = get_db_connection()
        if conn:
            cursor = conn.cursor()
            hashed_pass = hash_password(password)
            cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s",
                           (username, hashed_pass))
            user = cursor.fetchone()
            cursor.close()
            conn.close()

            if user:
                messagebox.showinfo("Success", "Login Successful!")
                self.root.destroy()
                open_dashboard()
            else:
                messagebox.showerror("Error", "Invalid username or password")

    def open_register(self):
        self.root.destroy()
        open_register()


# Register Page
class RegisterPage:
    def __init__(self, root):
        self.root = root
        self.root.title("Register - Employee Management System")
        self.root.geometry("400x600")
        self.root.resizable(False, False)
        self.root.configure(bg="#f0f9ff")

        # Center window
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - 400) // 2
        y = (screen_height - 600) // 2
        self.root.geometry(f"400x600+{x}+{y}")

        # Header
        header_frame = tk.Frame(root, bg="#1e40af", height=100)
        header_frame.pack(fill="x")

        tk.Label(header_frame, text="Register", font=("Arial", 24, "bold"),
                 bg="#1e40af", fg="white").pack(pady=30)

        # Main frame
        main_frame = tk.Frame(root, bg="#f0f9ff")
        main_frame.pack(pady=20)

        # Username
        tk.Label(main_frame, text="Username:", font=("Arial", 12),
                 bg="#f0f9ff").pack(anchor="w", pady=(10, 5))
        self.username_entry = tk.Entry(main_frame, font=("Arial", 12), width=30)
        self.username_entry.pack(pady=(0, 15))

        # Email
        tk.Label(main_frame, text="Email:", font=("Arial", 12),
                 bg="#f0f9ff").pack(anchor="w", pady=(10, 5))
        self.email_entry = tk.Entry(main_frame, font=("Arial", 12), width=30)
        self.email_entry.pack(pady=(0, 15))

        # Password
        tk.Label(main_frame, text="Password:", font=("Arial", 12),
                 bg="#f0f9ff").pack(anchor="w", pady=(10, 5))
        self.password_entry = tk.Entry(main_frame, font=("Arial", 12),
                                       width=30, show="*")
        self.password_entry.pack(pady=(0, 15))

        # Confirm Password
        tk.Label(main_frame, text="Confirm Password:", font=("Arial", 12),
                 bg="#f0f9ff").pack(anchor="w", pady=(10, 5))
        self.confirm_pass_entry = tk.Entry(main_frame, font=("Arial", 12),
                                           width=30, show="*")
        self.confirm_pass_entry.pack(pady=(0, 15))

        # Register button
        tk.Button(main_frame, text="Register", font=("Arial", 14, "bold"),
                  bg="#1e40af", fg="white", width=20,
                  command=self.register).pack(pady=20)

        # Login link
        tk.Label(main_frame, text="Already have an account?",
                 font=("Arial", 10), bg="#f0f9ff").pack()
        tk.Button(main_frame, text="Login Here", font=("Arial", 10, "underline"),
                  bg="#f0f9ff", fg="#1e40af", border=0,
                  command=self.open_login).pack()

    def register(self):
        username = self.username_entry.get()
        email = self.email_entry.get()
        password = self.password_entry.get()
        confirm_pass = self.confirm_pass_entry.get()

        if not username or not email or not password or not confirm_pass:
            messagebox.showerror("Error", "Please fill all fields")
            return

        if password != confirm_pass:
            messagebox.showerror("Error", "Passwords do not match")
            return

        if len(password) < 6:
            messagebox.showerror("Error", "Password must be at least 6 characters")
            return

        conn = get_db_connection()
        if conn:
            cursor = conn.cursor()
            try:
                hashed_pass = hash_password(password)
                cursor.execute("INSERT INTO users (username, password, email) VALUES (%s, %s, %s)",
                               (username, hashed_pass, email))
                conn.commit()
                messagebox.showinfo("Success", "Registration Successful! Please login.")
                self.open_login()
            except Error as e:
                messagebox.showerror("Error", f"Username already exists or {e}")
            finally:
                cursor.close()
                conn.close()

    def open_login(self):
        self.root.destroy()
        open_login()


# Dashboard
class Dashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("Dashboard - Employee Management System")
        self.root.geometry("1200x700")
        self.root.configure(bg="#f8fafc")

        # Header
        header = tk.Frame(root, bg="#1e40af", height=80)
        header.pack(fill="x")

        tk.Label(header, text="Employee Management Dashboard",
                 font=("Arial", 24, "bold"), bg="#1e40af", fg="white").pack(side="left", padx=20, pady=20)

        tk.Button(header, text="Logout", font=("Arial", 12), bg="#dc2626",
                  fg="white", command=self.logout).pack(side="right", padx=20)

        # Main container
        container = tk.Frame(root, bg="#f8fafc")
        container.pack(fill="both", expand=True, padx=20, pady=20)

        # Left panel - Form
        left_panel = tk.Frame(container, bg="white", relief="solid", borderwidth=1)
        left_panel.pack(side="left", fill="y", padx=(0, 10))

        tk.Label(left_panel, text="Employee Details", font=("Arial", 16, "bold"),
                 bg="white").pack(pady=20)

        # Form fields
        form_frame = tk.Frame(left_panel, bg="white")
        form_frame.pack(padx=20, pady=10)

        fields = ["Name", "Email", "Phone", "Department", "Position", "Salary", "Join Date (YYYY-MM-DD)"]
        self.entries = {}

        for field in fields:
            tk.Label(form_frame, text=field + ":", font=("Arial", 11),
                     bg="white").pack(anchor="w", pady=(10, 2))
            entry = tk.Entry(form_frame, font=("Arial", 11), width=30)
            entry.pack(pady=(0, 5))
            self.entries[field] = entry

        # Buttons
        btn_frame = tk.Frame(left_panel, bg="white")
        btn_frame.pack(pady=20)

        tk.Button(btn_frame, text="Add Employee", bg="#10b981", fg="white",
                  font=("Arial", 11), width=15, command=self.add_employee).pack(pady=5)
        tk.Button(btn_frame, text="Update Employee", bg="#f59e0b", fg="white",
                  font=("Arial", 11), width=15, command=self.update_employee).pack(pady=5)
        tk.Button(btn_frame, text="Delete Employee", bg="#dc2626", fg="white",
                  font=("Arial", 11), width=15, command=self.delete_employee).pack(pady=5)
        tk.Button(btn_frame, text="Clear Form", bg="#6b7280", fg="white",
                  font=("Arial", 11), width=15, command=self.clear_form).pack(pady=5)

        # Right panel - Table
        right_panel = tk.Frame(container, bg="white", relief="solid", borderwidth=1)
        right_panel.pack(side="right", fill="both", expand=True)

        tk.Label(right_panel, text="Employee List", font=("Arial", 16, "bold"),
                 bg="white").pack(pady=20)

        # Search
        search_frame = tk.Frame(right_panel, bg="white")
        search_frame.pack(pady=10)

        tk.Label(search_frame, text="Search:", font=("Arial", 11),
                 bg="white").pack(side="left", padx=5)
        self.search_entry = tk.Entry(search_frame, font=("Arial", 11), width=30)
        self.search_entry.pack(side="left", padx=5)
        tk.Button(search_frame, text="Search", bg="#1e40af", fg="white",
                  command=self.search_employee).pack(side="left", padx=5)
        tk.Button(search_frame, text="Show All", bg="#6b7280", fg="white",
                  command=self.load_employees).pack(side="left", padx=5)

        # Treeview
        tree_frame = tk.Frame(right_panel, bg="white")
        tree_frame.pack(fill="both", expand=True, padx=20, pady=10)

        scrollbar = ttk.Scrollbar(tree_frame)
        scrollbar.pack(side="right", fill="y")

        self.tree = ttk.Treeview(tree_frame, yscrollcommand=scrollbar.set,
                                 columns=("ID", "Name", "Email", "Phone", "Dept", "Position", "Salary", "Date"),
                                 show="headings", height=20)

        scrollbar.config(command=self.tree.yview)

        # Columns
        columns = [("ID", 50), ("Name", 120), ("Email", 150), ("Phone", 100),
                   ("Dept", 100), ("Position", 100), ("Salary", 80), ("Date", 100)]

        for col, width in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=width)

        self.tree.pack(fill="both", expand=True)
        self.tree.bind("<ButtonRelease-1>", self.select_employee)

        self.load_employees()

    def add_employee(self):
        data = {k: v.get() for k, v in self.entries.items()}

        if not all(data.values()):
            messagebox.showerror("Error", "Please fill all fields")
            return

        conn = get_db_connection()
        if conn:
            cursor = conn.cursor()
            try:
                cursor.execute("""
                    INSERT INTO employees (name, email, phone, department, position, salary, join_date)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, (data["Name"], data["Email"], data["Phone"], data["Department"],
                      data["Position"], data["Salary"], data["Join Date (YYYY-MM-DD)"]))
                conn.commit()
                messagebox.showinfo("Success", "Employee added successfully!")
                self.clear_form()
                self.load_employees()
            except Error as e:
                messagebox.showerror("Error", f"Error: {e}")
            finally:
                cursor.close()
                conn.close()

    def update_employee(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showerror("Error", "Please select an employee")
            return

        emp_id = self.tree.item(selected[0])['values'][0]
        data = {k: v.get() for k, v in self.entries.items()}

        if not all(data.values()):
            messagebox.showerror("Error", "Please fill all fields")
            return

        conn = get_db_connection()
        if conn:
            cursor = conn.cursor()
            try:
                cursor.execute("""
                    UPDATE employees SET name=%s, email=%s, phone=%s, department=%s, 
                    position=%s, salary=%s, join_date=%s WHERE emp_id=%s
                """, (data["Name"], data["Email"], data["Phone"], data["Department"],
                      data["Position"], data["Salary"], data["Join Date (YYYY-MM-DD)"], emp_id))
                conn.commit()
                messagebox.showinfo("Success", "Employee updated successfully!")
                self.clear_form()
                self.load_employees()
            except Error as e:
                messagebox.showerror("Error", f"Error: {e}")
            finally:
                cursor.close()
                conn.close()

    def delete_employee(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showerror("Error", "Please select an employee")
            return

        emp_id = self.tree.item(selected[0])['values'][0]

        if messagebox.askyesno("Confirm", "Are you sure you want to delete this employee?"):
            conn = get_db_connection()
            if conn:
                cursor = conn.cursor()
                try:
                    cursor.execute("DELETE FROM employees WHERE emp_id=%s", (emp_id,))
                    conn.commit()
                    messagebox.showinfo("Success", "Employee deleted successfully!")
                    self.clear_form()
                    self.load_employees()
                except Error as e:
                    messagebox.showerror("Error", f"Error: {e}")
                finally:
                    cursor.close()
                    conn.close()

    def load_employees(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        conn = get_db_connection()
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM employees")
            rows = cursor.fetchall()

            for row in rows:
                self.tree.insert("", "end", values=row[:8])

            cursor.close()
            conn.close()

    def search_employee(self):
        search_term = self.search_entry.get()

        for item in self.tree.get_children():
            self.tree.delete(item)

        conn = get_db_connection()
        if conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM employees WHERE name LIKE %s OR email LIKE %s 
                OR phone LIKE %s OR department LIKE %s
            """, (f"%{search_term}%", f"%{search_term}%", f"%{search_term}%", f"%{search_term}%"))
            rows = cursor.fetchall()

            for row in rows:
                self.tree.insert("", "end", values=row[:8])

            cursor.close()
            conn.close()

    def select_employee(self, event):
        selected = self.tree.selection()
        if selected:
            values = self.tree.item(selected[0])['values']
            fields = ["Name", "Email", "Phone", "Department", "Position", "Salary", "Join Date (YYYY-MM-DD)"]
            for i, field in enumerate(fields):
                self.entries[field].delete(0, tk.END)
                self.entries[field].insert(0, values[i + 1])

    def clear_form(self):
        for entry in self.entries.values():
            entry.delete(0, tk.END)

    def logout(self):
        if messagebox.askyesno("Logout", "Are you sure you want to logout?"):
            self.root.destroy()
            open_login()


# Main functions
def open_login():
    root = tk.Tk()
    LoginPage(root)
    root.mainloop()


def open_register():
    root = tk.Tk()
    RegisterPage(root)
    root.mainloop()


def open_dashboard():
    root = tk.Tk()
    Dashboard(root)
    root.mainloop()


# Main execution
if __name__ == "__main__":
    setup_database()
    root = tk.Tk()
    SplashScreen(root)
    root.mainloop()