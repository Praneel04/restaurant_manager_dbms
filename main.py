import tkinter as tk
from tkinter import ttk, messagebox, StringVar
import mysql.connector
from user import manage_users
# Import necessary modules
from menu import show_menu
from order import show_orders
from place_order_page import place_order
from customers import show_customers
from staff import show_staff
from reservation import reservation_page
# Establish database connection
con = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Sepaugtf25",  # Replace with your actual password
    database="newrest1"  # Replace with your database
)

def menu_page():
    show_menu(con)

def order_page():
    show_orders(con)

def placeorder_page():
    place_order(con)

def customers_page():
    show_customers(con)

def staff_page():
    show_staff(con)
def users_page():
    manage_users(con)
def reservations():
    reservation_page(con)
def enter():
    # Create a new window for options
    root = tk.Toplevel()
    root.title("Restaurant Management - Dashboard")
    root.geometry("600x400")
    root.configure(bg="#f4f4f4")

    # Add title label
    ttk.Label(root, text="Restaurant Management System", font=("Helvetica", 16, "bold")).pack(pady=10)

    # Frame for buttons
    button_frame = ttk.Frame(root, padding=10)
    button_frame.pack(expand=True)

    # Add buttons with consistent style
    ttk.Button(button_frame, text="Orders", command=order_page).grid(row=0, column=0, padx=20, pady=10)
    ttk.Button(button_frame, text="Staff", command=staff_page).grid(row=0, column=1, padx=20, pady=10)
    ttk.Button(button_frame, text="Menu", command=menu_page).grid(row=1, column=0, padx=20, pady=10)
    ttk.Button(button_frame, text="Place Order", command=placeorder_page).grid(row=1, column=1, padx=20, pady=10)
    ttk.Button(button_frame, text="Customers", command=customers_page).grid(row=2, column=0, padx=20, pady=10)
    ttk.Button(button_frame, text="users", command=users_page).grid(row=2, column=1, padx=20, pady=10)
    ttk.Button(button_frame, text="reservation", command=reservations).grid(row=3, column=0, padx=20, pady=10)
    # Optional: Add more buttons as needed
    # ttk.Button(button_frame, text="Feedback", command=show_feedback).grid(row=2, column=1, padx=20, pady=10)

    root.mainloop()

def submit():
    username = a.get().strip()
    password = b.get().strip()
    if not username or not password:
        messagebox.showwarning("Input Error", "Please enter both username and password.")
        return
    try:
        cur = con.cursor()
        cur.execute("SELECT * FROM admin WHERE username = %s AND password = %s", (username, password))
        result = cur.fetchone()
        if result:
            messagebox.showinfo("Login Successful", "Welcome!")
            enter()
        else:
            messagebox.showwarning("Login Failed", "Invalid username or password.")
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")

# Main Login Page
r = tk.Tk()
r.title("Login - Restaurant Management System")
r.geometry("400x300")
r.configure(bg="#f4f4f4")
a = StringVar()
b = StringVar()

# Title label
ttk.Label(r, text="RESTAURANT ADMIN LOGIN", font=("Helvetica", 14, "bold")).pack(pady=20)

# Username entry
ttk.Label(r, text="USERNAME:").place(x=100, y=100)
username_entry = ttk.Entry(r, textvariable=a)
username_entry.place(x=170, y=100)

# Password entry
ttk.Label(r, text="PASSWORD:").place(x=100, y=140)
password_entry = ttk.Entry(r, textvariable=b, show="*")
password_entry.place(x=170, y=140)

# Submit button
ttk.Button(r, text="SUBMIT", command=submit).place(x=170, y=180)

r.mainloop()
