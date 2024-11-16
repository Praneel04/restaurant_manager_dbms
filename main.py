import tkinter as tk
from tkinter import ttk, messagebox, StringVar, IntVar, Toplevel, Label, Entry, Button, Frame
import mysql.connector
from feedback import show_feedback
from menu import show_menu
from order import show_orders

con = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Sepaugtf25",  # Replace with your actual password
    database="newrest1"  # Replace with your database
)
# def show_menu():
#     # Code to display the menu page
#     pass

def order_page():
    # Code to display the orders page
    show_orders(con)
    pass

# def show_delivery():
#     # Code to display the delivery page
#     pass

# def show_sales():
#     # Code to display the sales page
#     pass

# def show_feedback():
#     # Code to display the feedback page
#     pass

def enter():
    # Create a new window
    root = tk.Toplevel()  # Use Toplevel to create a new window while keeping the main window active
    root.title("OPtions")
    root.geometry("400x300")

    # Add buttons for different functionalities
    Button(root, text="Orders", command=order_page).place(x=150, y=100)

    # Add more buttons as needed (commented out here)
    # Button(root, text="Menu", command=show_menu).place(x=50, y=150)
    # Button(root, text="Delivery", command=show_delivery).place(x=250, y=150)
    # Button(root, text="Sales", command=show_sales).place(x=350, y=150)
    # Button(root, text="Feedback", command=show_feedback).place(x=450, y=150)

    root.mainloop()

flag=0
def submit():
    username = a.get()
    password = b.get()
    if not username or not password:
        messagebox.showwarning("Input Error", "Please enter both username and password.")
        return
    try:
        cur = con.cursor()
        cur.execute("SELECT * FROM admin WHERE username = %s AND password = %s", (username, password))
        result = cur.fetchone()
        if result:
            messagebox.showinfo("Login Successful", "Welcome!")
            flag=1
            enter()
        else:
            messagebox.showwarning("Login Failed", "Invalid username or password.")
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")
# if(flag==1):
#     enter()
# else:
#     print("NO entry")
r = tk.Tk()
r.title("LOGIN RESTAURANT MANAGEMENT SYSTEM")
r.geometry("400x300")
a = StringVar()
b = StringVar()
Label(r, text="RESTAURANT ADMIN LOGIN").pack()
Label(r, text="USERNAME").place(x=100, y=100)
Entry(r, textvariable=a).place(x=170, y=100)
Label(r, text="PASSWORD").place(x=100, y=140)
Entry(r, textvariable=b, show="*").place(x=170, y=140)
Button(r, text="SUBMIT", command=submit).place(x=180, y=180)
con.commit()
r.mainloop()