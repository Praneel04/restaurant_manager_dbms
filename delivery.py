import tkinter as tk
from tkinter import ttk, messagebox, StringVar, IntVar, Toplevel, Label, Entry, Button, Frame
def show_orders(con):
    root = Toplevel()
    root.title("Order Management")

    tree = ttk.Treeview(root, columns=("order_id", "customer_name", "total_amount", "order_time"), show="headings")
    tree.heading("order_id", text="Order ID")
    tree.heading("customer_name", text="Customer Name")
    tree.heading("total_amount", text="Total Amount")
    tree.heading("order_time", text="Order Time")
    tree.pack()

    def refresh_orders():
        for row in tree.get_children():
            tree.delete(row)
        cur = con.cursor()
        query = """
            SELECT o.Order_id, c.Name, o.Amount, o.Time
            FROM `Order` o
            JOIN Customer c ON o.Customer_id = c.Customer_id
        """
        cur.execute(query)
        orders = cur.fetchall()
        for order in orders:
            tree.insert('', 'end', values=order)

    Button(root, text="Refresh Orders", command=refresh_orders).place(x=250, y=400)
    refresh_orders()

    root.mainloop()