import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import Calendar
from datetime import datetime
from customers import show_customers

def reservation_page(con):
    root = tk.Toplevel()
    root.title("Reservation Page")
    
    root.configure(bg="#f4f4f4")

    

    

    # Load available tables
    cur = con.cursor()
    cur.execute("SELECT Table_id, Total_people FROM `Tables` WHERE IsOccupied = FALSE")
    available_tables = cur.fetchall()

    # Load available customers
    cur.execute("SELECT Customer_id, Name FROM Customer")
    available_customers = cur.fetchall()

    ttk.Label(root, text="Reservation System", font=("Helvetica", 20, "bold"), background="#f4f4f4").pack(pady=15)

    # Frame for form elements
    form_frame = ttk.Frame(root)
    form_frame.pack(pady=20, padx=30, fill="x")

    # Customer selection
    ttk.Label(form_frame, text="Select Customer:", font=("Helvetica", 12)).grid(row=0, column=0, sticky="w", pady=10, padx=10)
    selected_customer = tk.StringVar()
    customer_dropdown = ttk.Combobox(form_frame, textvariable=selected_customer, state="readonly", width=40)
    customer_dropdown['values'] = [f"{customer[0]} - {customer[1]}" for customer in available_customers]
    customer_dropdown.grid(row=0, column=1, padx=10, pady=10)

    # Table selection
    ttk.Label(form_frame, text="Select Table:", font=("Helvetica", 12)).grid(row=1, column=0, sticky="w", pady=10, padx=10)
    selected_table = tk.StringVar()
    table_dropdown = ttk.Combobox(form_frame, textvariable=selected_table, state="readonly", width=40)
    table_dropdown['values'] = [f"{table[0]} (Capacity: {table[1]})" for table in available_tables]
    table_dropdown.grid(row=1, column=1, padx=10, pady=10)

    # Number of people entry
    ttk.Label(form_frame, text="Number of People:", font=("Helvetica", 12)).grid(row=2, column=0, sticky="w", pady=10, padx=10)
    num_people_entry = tk.Entry(form_frame, width=15)
    num_people_entry.grid(row=2, column=1, padx=10, pady=10, sticky="w")

    # Calendar widget for date selection
    ttk.Label(form_frame, text="Select Reservation Date:", font=("Helvetica", 12)).grid(row=3, column=0, sticky="w", pady=10, padx=10)
    calendar = Calendar(form_frame, selectmode='day', date_pattern='yyyy-mm-dd')
    calendar.grid(row=3, column=1, padx=10, pady=10, sticky="w")

    # Time selection using comboboxes
    ttk.Label(form_frame, text="Select Time:", font=("Helvetica", 12)).grid(row=4, column=0, sticky="w", pady=10, padx=10)
    time_frame = ttk.Frame(form_frame)
    time_frame.grid(row=4, column=1, padx=10, pady=10, sticky="w")
    hours = [f"{hour:02}" for hour in range(24)]
    minutes = [f"{minute:02}" for minute in range(0, 60, 5)]

    selected_hour = tk.StringVar(value="12")
    selected_minute = tk.StringVar(value="00")
    hour_dropdown = ttk.Combobox(time_frame, textvariable=selected_hour, values=hours, state="readonly", width=3)
    minute_dropdown = ttk.Combobox(time_frame, textvariable=selected_minute, values=minutes, state="readonly", width=3)
    hour_dropdown.grid(row=0, column=0, padx=(0, 5))
    minute_dropdown.grid(row=0, column=1)

    # Function to make a reservation
    def make_reservation():
        customer_id = selected_customer.get().split(' - ')[0].strip() if selected_customer.get() else None
        table_info = selected_table.get()
        num_people = num_people_entry.get().strip()
        reservation_date = calendar.get_date()
        reservation_time = f"{selected_hour.get()}:{selected_minute.get()}:00"

        if not customer_id or not table_info or not num_people or not reservation_date or not reservation_time:
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
            # Combine date and time for full datetime string
            reservation_datetime = f"{reservation_date} {reservation_time}"

            # Call the stored procedure to make the reservation
            cur.callproc('MakeReservation', [table_id, customer_id, reservation_datetime, num_people])
            con.commit()

            messagebox.showinfo("Success", "Reservation made successfully.")
            root.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Error: {e}")

    # Submit button
    ttk.Button(root, text="Make Reservation", command=make_reservation, style="Accent.TButton").pack(pady=15)
    ttk.Button(root, text="New Customer", command=lambda: show_customers(con), style="Accent.TButton").pack(pady=10)

    # Custom Button Style
    style = ttk.Style()
    style.configure("Accent.TButton", font=("Helvetica", 12), padding=8, background="#4caf50", foreground="white", borderwidth=3)
    style.map("Accent.TButton", background=[("active", "#388e3c")])

    root.mainloop()
