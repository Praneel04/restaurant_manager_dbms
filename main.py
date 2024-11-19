import tkinter as tk
from tkinter import ttk, messagebox, StringVar
import mysql.connector
from user import manage_users
from menu import show_menu
from order import show_orders
from place_order_page import place_order
from customers import show_customers
from staff import show_staff
from res_page import show_reservations
from tables import show_tables
from sales import sales_page
# Database connection
con = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Sepaugtf25",  # Replace with your actual password
    database="newrest1"
)

def menu_page(): show_menu(con)
def order_page(): show_orders(con)
def placeorder_page(): place_order(con)
def customers_page(): show_customers(con)
def staff_page(): show_staff(con)
def users_page(): manage_users(con)
def reservations(): show_reservations(con)
def tables_page(): show_tables(con)
def sales(): sales_page(con)
def enter():
    root = tk.Toplevel()
    root.title("Restaurant Management - Dashboard")
    root.configure(bg="#2d2f3b")


    # Styling
    bg_color = "#282c34"  # Dark background for contrast
    title_color = "#61dafb"  # Light blue for contrast
    button_color = "#007BFF"
    button_hover_color = "#0056b3"
    text_color = "#f8f9fa"  # Light text for readability
    button_font = ("Helvetica", 12, "bold")

    root.configure(bg=bg_color)

    # Title label
    title_label = tk.Label(root, text="Restaurant Management System", font=("Helvetica", 24, "bold"), bg=bg_color, fg=title_color)
    title_label.pack(pady=20)

    # Frame for buttons
    button_frame = tk.Frame(root, bg=bg_color, pady=10)
    button_frame.pack(expand=True)

    # Button Configuration
    buttons = [
        ("Orders", order_page),
        ("Staff", staff_page),
        ("Menu", menu_page),
        ("Place Order", placeorder_page),
        ("Customers", customers_page),
        ("Users", users_page),
        ("Reservations", reservations),
        ("Tables", tables_page),
        ("Sales", sales)
    ]

    def on_enter(event):
        event.widget['background'] = button_hover_color

    def on_leave(event):
        event.widget['background'] = button_color

    for idx, (text, command) in enumerate(buttons):
        btn = tk.Button(
            button_frame, text=text, command=command, font=button_font,
            bg=button_color, fg=text_color, activebackground=button_hover_color,
            activeforeground="white", relief="raised", bd=2, width=20
        )
        btn.grid(row=idx // 2, column=idx % 2, padx=20, pady=10)
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)

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
            r.destroy()
            enter()
        else:
            messagebox.showwarning("Login Failed", "Invalid username or password.")
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")

# Main Login Page
r = tk.Tk()
r.title("Login - Restaurant Management System")
bg_color = "#343a40"  # Dark background
text_color = "#f8f9fa"  # Light text for readability
r.configure(bg=bg_color)

a = StringVar()
b = StringVar()

# Title label
ttk.Label(r, text="RESTAURANT ADMIN LOGIN", font=("Helvetica", 20, "bold"), background=bg_color, foreground=text_color).pack(pady=40)

# Username entry
username_frame = tk.Frame(r, bg=bg_color)
username_frame.pack(pady=10)
ttk.Label(username_frame, text="USERNAME:", background=bg_color, foreground=text_color).pack(side=tk.LEFT, padx=10)
username_entry = ttk.Entry(username_frame, textvariable=a, font=("Helvetica", 12))
username_entry.pack(side=tk.LEFT)

# Password entry
password_frame = tk.Frame(r, bg=bg_color)
password_frame.pack(pady=10)
ttk.Label(password_frame, text="PASSWORD:", background=bg_color, foreground=text_color).pack(side=tk.LEFT, padx=10)
password_entry = ttk.Entry(password_frame, textvariable=b, show="*", font=("Helvetica", 12))
password_entry.pack(side=tk.LEFT)

# Submit button
submit_button = tk.Button(r, text="SUBMIT", command=submit, font=("Helvetica", 14, "bold"), bg="#28a745", fg="white", activebackground="#218838", relief="raised", bd=3)
submit_button.pack(pady=20)

r.mainloop()
