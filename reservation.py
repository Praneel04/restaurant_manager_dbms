import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from customers import show_customers
def reservation_page(con):
    db = con
    root = tk.Toplevel()
    root.title("Reservation Page")
    root.geometry("600x500")
    root.configure(bg="#f4f4f4")

    # Load available tables
    cur = con.cursor()
    cur.execute("SELECT Table_id, Total_people FROM `Table` WHERE IsOccupied = FALSE")
    available_tables = cur.fetchall()

    # Load available customers
    cur.execute("SELECT Customer_id, Name FROM Customer")
    available_customers = cur.fetchall()

    ttk.Label(root, text="Reservation System", font=("Helvetica", 16, "bold")).pack(pady=10)

    # Customer selection
    ttk.Label(root, text="Select Customer:").pack(pady=5)
    selected_customer = tk.StringVar()
    customer_dropdown = ttk.Combobox(root, textvariable=selected_customer, state="readonly")
    customer_dropdown['values'] = [f"{customer[0]} - {customer[1]}" for customer in available_customers]
    customer_dropdown.pack(pady=5)

    # Table selection
    ttk.Label(root, text="Select Table:").pack(pady=5)
    selected_table = tk.StringVar()
    table_dropdown = ttk.Combobox(root, textvariable=selected_table, state="readonly")
    table_dropdown['values'] = [f"{table[0]} (Capacity: {table[1]})" for table in available_tables]
    table_dropdown.pack(pady=5)

    # Number of people entry
    ttk.Label(root, text="Number of People:").pack(pady=5)
    num_people_entry = tk.Entry(root)
    num_people_entry.pack(pady=5)

    # Reservation time entry
    ttk.Label(root, text="Reservation Time (YYYY-MM-DD HH:MM:SS):").pack(pady=5)
    time_entry = tk.Entry(root)
    time_entry.pack(pady=5)

    # Function to make a reservation
    def make_reservation():
        customer_id = selected_customer.get().split(' - ')[0].strip() if selected_customer.get() else None
        table_info = selected_table.get()
        num_people = num_people_entry.get().strip()
        reservation_time = time_entry.get().strip()

        if not customer_id or not table_info or not num_people or not reservation_time:
            messagebox.showwarning("Input Error", "Please fill in all fields.")
            return

        try:
            table_id = int(table_info.split(' ')[0].strip())
            max_capacity = int(table_info.split('(')[1].split(': ')[1].split(')')[0].strip())
            num_people = int(num_people)
            if num_people > max_capacity:
                messagebox.showerror("Capacity Error", f"The selected table can only accommodate up to {max_capacity} people.")
                return
        except ValueError:
            messagebox.showerror("Input Error", "Invalid number of people or table selection.")
            return

        try:
            # Check date and time validity
            datetime.strptime(reservation_time, '%Y-%m-%d %H:%M:%S')

            # Make the reservation
            
            cur.callproc('MakeReservation', [table_id, customer_id, reservation_time, num_people])
            con.commit()

            # Mark the table as occupied
            cur.execute("UPDATE `Table` SET IsOccupied = 1 WHERE Table_id = %s", (table_id,))
            con.commit()

            messagebox.showinfo("Success", "Reservation made successfully.")
            root.destroy()
        except ValueError:
            messagebox.showerror("Invalid Date/Time", "Please enter a valid date and time.")
        
    
    
    # Submit button
    ttk.Button(root, text="Make Reservation", command=make_reservation).pack(pady=20)
    ttk.Button(root, text="New Customer", command=lambda: show_customers(con)).pack(pady=20)
    root.mainloop()
