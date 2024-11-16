import tkinter as tk
from tkinter import ttk, messagebox

def place_order(con):
    root = tk.Toplevel()
    root.title("Place Order")
    root.geometry("750x600")

    # Load menu items from the database
    cur = con.cursor()
    cur.execute("SELECT Item_id, Name, Price FROM Item")
    menu_items = cur.fetchall()

    # Load available tables
    cur.execute("SELECT Table_id FROM `table` WHERE IsOccupied = FALSE")
    available_tables = [row[0] for row in cur.fetchall()]

    # Load available staff
    cur.execute("SELECT Staff_id, Name FROM Staff")
    available_staff = cur.fetchall()

    # Frame for displaying menu with quantity inputs
    menu_frame = tk.Frame(root)
    menu_frame.place(x=20, y=20, width=700, height=250)

    # Scrollable canvas for the menu
    canvas = tk.Canvas(menu_frame)
    scrollbar = tk.Scrollbar(menu_frame, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas)

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # Dictionary to hold quantity inputs
    item_vars = {}
    for item in menu_items:
        item_id, name, price = item
        item_frame = tk.Frame(scrollable_frame)
        item_frame.pack(fill="x", padx=5, pady=2)

        tk.Label(item_frame, text=f"{name} (ID: {item_id}, Price: {price})", anchor="w", width=40).pack(side="left")
        quantity_var = tk.IntVar(value=0)  # Default quantity is 0
        quantity_entry = tk.Spinbox(item_frame, from_=0, to=100, textvariable=quantity_var, width=5)
        quantity_entry.pack(side="right")

        # Map item_id to quantity variable and other details
        item_vars[item_id] = (quantity_var, name, price)

    # Frame for order details
    order_frame = tk.Frame(root, bg="#f0f0f0", bd=2, relief="solid")
    order_frame.place(x=20, y=300, width=700, height=200)

    tk.Label(order_frame, text="Customer ID:", font=("Helvetica", 10), bg="#f0f0f0").place(x=10, y=10)
    customer_id_entry = tk.Entry(order_frame, width=15, font=("Helvetica", 10))
    customer_id_entry.place(x=100, y=10)

    # Dropdown for selecting table
    tk.Label(order_frame, text="Select Table:", font=("Helvetica", 10), bg="#f0f0f0").place(x=10, y=50)
    selected_table = tk.IntVar()
    table_dropdown = ttk.Combobox(order_frame, textvariable=selected_table, state="readonly")
    table_dropdown['values'] = available_tables
    table_dropdown.place(x=100, y=50)

    # Dropdown for selecting staff
    tk.Label(order_frame, text="Select Staff:", font=("Helvetica", 10), bg="#f0f0f0").place(x=300, y=50)
    selected_staff = tk.StringVar()
    staff_dropdown = ttk.Combobox(order_frame, textvariable=selected_staff, state="readonly")
    staff_dropdown['values'] = [f"{staff[0]} - {staff[1]}" for staff in available_staff]
    staff_dropdown.place(x=400, y=50)

    # Label to display selected items summary
    selected_items_label = tk.Label(order_frame, text="Selected Items:", bg="#f0f0f0", justify="left", font=("Helvetica", 10))
    selected_items_label.place(x=10, y=90)

    # Function to calculate and display selected items
    def update_selected_items():
        selected_items = [(item_id, details[1], details[2], details[0].get()) for item_id, details in item_vars.items() if details[0].get() > 0]
        selected_items_list = [f"{item[1]} (ID: {item[0]}, Price: {item[2]}, Qty: {item[3]})" for item in selected_items]

        if selected_items:
            selected_items_label.config(text="Selected Items:\n" + "\n".join(selected_items_list))
        else:
            selected_items_label.config(text="Selected Items:")

    # Add a button to update the selected items summary
    tk.Button(order_frame, text="Update Selection", command=update_selected_items, bg="#4caf50", fg="white").place(x=400, y=10)

    # Function to place the order
    def handle_order_placement():
        customer_id = customer_id_entry.get().strip()
        table_id = selected_table.get()
        staff_id = selected_staff.get().split(' - ')[0] if selected_staff.get() else None
        if not customer_id:
            messagebox.showwarning("Input Error", "Please provide a Customer ID.")
            return
        if not table_id:
            messagebox.showwarning("Input Error", "Please select a table.")
            return
        if not staff_id:
            messagebox.showwarning("Input Error", "Please select a staff member.")
            return

        selected_items = [(item_id, details[1], details[2], details[0].get()) for item_id, details in item_vars.items() if details[0].get() > 0]
        if not selected_items:
            messagebox.showwarning("Order Error", "No items selected for the order.")
            return

        cur = con.cursor()

        # Calculate total amount for the order
        total_amount = sum(float(item[2]) * item[3] for item in selected_items)  # Price * Quantity

        # Insert the order into the Orders table
        cur.execute("INSERT INTO Orders (CustomerID, TotalAmount, OrderTime, Status, Notes, StaffID, TableID) VALUES (%s, %s, NOW(), 'Pending', '', %s, %s)", (customer_id, total_amount, staff_id, table_id))
        con.commit()
        order_id = cur.lastrowid

        # Insert each ordered item into the OrderDetails table
        for item in selected_items:
            quantity = item[3]
            unit_price = float(item[2])
            total_price = unit_price * quantity
            cur.execute("INSERT INTO OrderDetails (OrderID, ItemID, Quantity, UnitPrice, TotalPrice) VALUES (%s, %s, %s, %s, %s)", (order_id, item[0], quantity, unit_price, total_price))
        con.commit()

        # Mark the table as occupied
        cur.execute("UPDATE `Table` SET IsOccupied = TRUE WHERE Table_id = %s", (table_id,))
        con.commit()

        messagebox.showinfo("Success", f"Order placed successfully! Order ID: {order_id}")
        customer_id_entry.delete(0, 'end')
        for var in item_vars.values():
            var[0].set(0)  # Reset all quantities to 0
        selected_items_label.config(text="Selected Items:")

    tk.Button(root, text="Place Order", command=handle_order_placement, bg="#2196f3", fg="white", font=("Helvetica", 12)).place(x=280, y=520)

    root.mainloop()
