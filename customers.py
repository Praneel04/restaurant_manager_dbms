import tkinter as tk
from tkinter import ttk, messagebox

def show_customers(con):
    root = tk.Toplevel()
    root.title("Customer Management")
    root.geometry("900x400")

    # Treeview to display customers
    customer_tree = ttk.Treeview(root, columns=("CustomerID", "Name", "Email", "Phone"), show="headings")
    customer_tree.heading("CustomerID", text="Customer ID")
    customer_tree.heading("Name", text="Name")
    customer_tree.heading("Email", text="Email")
    customer_tree.heading("Phone", text="Phone")
    customer_tree.column("CustomerID", width=100, anchor="center")
    customer_tree.column("Name", width=200, anchor="center")
    customer_tree.column("Email", width=250, anchor="center")
    customer_tree.column("Phone", width=150, anchor="center")
    customer_tree.pack(fill="both", expand=True, padx=10, pady=10)

    # Fetch customers from the database
    cur = con.cursor()
    cur.execute("SELECT Customer_id, Name, Email, Phone FROM Customer")
    customers = cur.fetchall()

    for customer in customers:
        customer_tree.insert('', 'end', values=customer)

    # Function to add a new customer
    def add_customer():
        name = name_entry.get().strip()
        email = email_entry.get().strip()
        phone = phone_entry.get().strip()

        if not name or not email:
            messagebox.showwarning("Input Error", "Please provide both Name and Email.")
            return

        try:
            cur.execute("INSERT INTO Customer (Name, Email, Phone) VALUES (%s, %s, %s)", (name, email, phone))
            con.commit()
            customer_id = cur.lastrowid
            customer_tree.insert('', 'end', values=(customer_id, name, email, phone))
            messagebox.showinfo("Success", "Customer added successfully!")
            name_entry.delete(0, 'end')
            email_entry.delete(0, 'end')
            phone_entry.delete(0, 'end')
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    # Function to remove a selected customer
    def remove_customer():
        selected = customer_tree.selection()
        if not selected:
            messagebox.showwarning("Selection Error", "Please select a customer to remove.")
            return

        confirm = messagebox.askyesno("Confirm Deletion", "Are you sure you want to remove the selected customer?")
        if confirm:
            for item in selected:
                customer_id = customer_tree.item(item, "values")[0]
                try:
                    cur.execute("DELETE FROM Customer WHERE Customer_id = %s", (customer_id,))
                    con.commit()
                    customer_tree.delete(item)
                    messagebox.showinfo("Success", "Customer removed successfully!")
                except Exception as e:
                    messagebox.showerror("Error", f"An error occurred: {e}")

    # Frame for adding new customer
    add_frame = tk.Frame(root)
    add_frame.pack(pady=10)

    tk.Label(add_frame, text="Name:").grid(row=0, column=0, padx=5, pady=5)
    name_entry = tk.Entry(add_frame)
    name_entry.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(add_frame, text="Email:").grid(row=0, column=2, padx=5, pady=5)
    email_entry = tk.Entry(add_frame)
    email_entry.grid(row=0, column=3, padx=5, pady=5)

    tk.Label(add_frame, text="Phone:").grid(row=0, column=4, padx=5, pady=5)
    phone_entry = tk.Entry(add_frame)
    phone_entry.grid(row=0, column=5, padx=5, pady=5)

    tk.Button(add_frame, text="Add Customer", command=add_customer, bg="#4caf50", fg="white").grid(row=0, column=6, padx=10, pady=5)

    # Button for removing a customer
    tk.Button(root, text="Remove Selected Customer", command=remove_customer, bg="#f44336", fg="white").pack(pady=10)

    root.mainloop()
