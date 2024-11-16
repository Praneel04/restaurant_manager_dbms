import tkinter as tk
from tkinter import ttk, messagebox, StringVar, IntVar, Toplevel, Label, Entry, Button, Frame
def show_sales(con):
    root = Toplevel()
    root.title("Sales Report")

    # Display sales summary
    total_revenue = 0
    total_orders = 0
    cur = con.cursor()
    cur.execute("SELECT SUM(Amount) AS total_revenue, COUNT(*) AS total_orders FROM `Order`")
    sales_summary = cur.fetchone()
    total_revenue = sales_summary[0]
    total_orders = sales_summary[1]

    Label(root, text=f"Total Revenue: ${total_revenue:.2f}").place(x=50, y=50)
    Label(root, text=f"Total Orders: {total_orders}").place(x=50, y=75)

    # Display top selling items
    tree = ttk.Treeview(root, columns=("item_name", "total_sold", "total_revenue"), show="headings")
    tree.heading("item_name", text="Item Name")
    tree.heading("total_sold", text="Total Sold")
    tree.heading("total_revenue", text="Total Revenue")
    tree.place(x=50, y=100)

    cur.execute("""
        SELECT i.Name, SUM(oi.Quantity) AS total_sold, SUM(oi.Quantity * i.Price) AS total_revenue
        FROM OrderItem oi
        JOIN Item i ON oi.Item_id = i.Item_id
        GROUP BY i.Item_id
        ORDER BY total_revenue DESC
        LIMIT 5
    """)
    top_items = cur.fetchall()
    for item in top_items:
        tree.insert('', 'end', values=item)

    root.mainloop()