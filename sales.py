import tkinter as tk
from tkinter import ttk
import mysql.connector
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

def sales_page(conn):

    def calculate_totals():
        total_sales = 0
        total_orders = len(tree.get_children())
        orders_per_staff = {}
        for child in tree.get_children():
            values = tree.item(child, 'values')
            total_sales += float(values[2])
            staff_id = values[5]
            if staff_id in orders_per_staff:
                orders_per_staff[staff_id] += 1
            else:
                orders_per_staff[staff_id] = 1
        
        total_label.config(text=f"Total Sales: ${total_sales:.2f}")
        orders_label.config(text=f"Total Orders: {total_orders}")
        
        # Display sales summary with a bar chart
        figure = Figure(figsize=(5, 4), dpi=100)
        ax = figure.add_subplot(111)
        staff_ids = list(orders_per_staff.keys())
        orders_count = list(orders_per_staff.values())
        ax.bar(staff_ids, orders_count, color=np.random.rand(len(staff_ids), 3))
        ax.set_xlabel('Staff ID')
        ax.set_ylabel('Number of Orders')
        ax.set_title('Orders Completed by Each Staff Member')

        canvas = FigureCanvasTkAgg(figure, root)
        canvas.get_tk_widget().pack()

    def display_average_order_value():
        total_sales = 0
        total_orders = len(tree.get_children())
        for child in tree.get_children():
            total_sales += float(tree.item(child, 'values')[2])
        
        if total_orders > 0:
            avg_order_value = total_sales / total_orders
        else:
            avg_order_value = 0
        
        avg_order_label.config(text=f"Average Order Value: ${avg_order_value:.2f}")

    # Setting up the Tkinter Window
    root = tk.Tk()
    root.title("Sales Page - Completed Orders")

    # Treeview for showing orders
    tree = ttk.Treeview(root, columns=("OrderID", "CustomerID", "TotalAmount", "OrderTime", "Status", "StaffID", "TableID"), show='headings')
    tree.heading("OrderID", text="Order ID")
    tree.heading("CustomerID", text="Customer ID")
    tree.heading("TotalAmount", text="Total Amount")
    tree.heading("OrderTime", text="Order Time")
    tree.heading("Status", text="Status")
    tree.heading("StaffID", text="Staff ID")
    tree.heading("TableID", text="Table ID")

    tree.pack(fill=tk.BOTH, expand=True)

    # Load data from connection
    cursor = conn.cursor()
    cursor.execute("SELECT OrderID, CustomerID, TotalAmount, OrderTime, Status, StaffID, TableID FROM Orders WHERE Status = 'Completed'")
    rows = cursor.fetchall()
    for row in rows:
        tree.insert("", "end", values=row)
    
    # Summary Labels
    total_label = tk.Label(root, text="Total Sales: $0.00")
    total_label.pack()

    orders_label = tk.Label(root, text="Total Orders: 0")
    orders_label.pack()

    avg_order_label = tk.Label(root, text="Average Order Value: $0.00")
    avg_order_label.pack()

    # Calculate Totals Button
    totals_button = tk.Button(root, text="Calculate Totals", command=lambda: [calculate_totals(), display_average_order_value()])
    totals_button.pack()

    root.mainloop()
