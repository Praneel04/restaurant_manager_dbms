import tkinter as tk
from tkinter import ttk, messagebox
from feedback import feedback_page

def show_orders(con):
    root = tk.Toplevel()
    root.title("Order Management")
    
    
    

    # Tabs for separating pending and paid/done orders
    tab_control = ttk.Notebook(root)
    pending_tab = ttk.Frame(tab_control)
    done_tab = ttk.Frame(tab_control)
    tab_control.add(pending_tab, text="Pending Orders")
    tab_control.add(done_tab, text="Paid/Done Orders")
    tab_control.pack(expand=1, fill="both")

    # Style Treeviews
    style = ttk.Style()
    style.theme_use("clam")  # Modern-looking theme
    style.configure("Treeview", rowheight=30, font=("Helvetica", 11), background="#f2f2f2", fieldbackground="#f2f2f2")
    style.configure("Treeview.Heading", font=("Helvetica", 13, "bold"), background="#4CAF50", foreground="white")
    
    # Pending Orders Treeview
    pending_tree = ttk.Treeview(pending_tab, columns=("OrderID", "Items", "ItemDetails", "TotalAmount"), show="headings")
    for col in ("OrderID", "Items", "ItemDetails", "TotalAmount"):
        pending_tree.heading(col, text=col, anchor="center")
        pending_tree.column(col, anchor="center")
    pending_tree.column("OrderID", width=100)
    pending_tree.column("Items", width=250)
    pending_tree.column("ItemDetails", width=350)
    pending_tree.column("TotalAmount", width=100)
    pending_tree.pack(fill="both", expand=True, padx=20, pady=20)

    # Paid/Done Orders Treeview
    done_tree = ttk.Treeview(done_tab, columns=("OrderID", "Items", "ItemDetails", "TotalAmount"), show="headings")
    for col in ("OrderID", "Items", "ItemDetails", "TotalAmount"):
        done_tree.heading(col, text=col, anchor="center")
        done_tree.column(col, anchor="center")
    done_tree.column("OrderID", width=100)
    done_tree.column("Items", width=250)
    done_tree.column("ItemDetails", width=350)
    done_tree.column("TotalAmount", width=100)
    done_tree.pack(fill="both", expand=True, padx=20, pady=20)

    # Fetch pending orders
    cur = con.cursor()
    query_pending = """
        SELECT 
            od.OrderID,
            GROUP_CONCAT(i.Name SEPARATOR ', ') AS Items,
            GROUP_CONCAT(CONCAT(i.Name, ' (Qty: ', od.Quantity, ', Unit Price: ', od.UnitPrice, ')') SEPARATOR '\n') AS ItemDetails,
            SUM(od.TotalPrice) AS TotalAmount
        FROM 
            OrderDetails od
        JOIN 
            Orders o ON od.OrderID = o.OrderID
        JOIN 
            Item i ON od.ItemID = i.Item_id
        WHERE 
            o.Status = 'Pending'
        GROUP BY 
            od.OrderID;
    """
    cur.execute(query_pending)
    pending_orders = cur.fetchall()

    for order in pending_orders:
        pending_tree.insert('', 'end', values=order)

    # Fetch paid/done orders
    query_done = """
        SELECT 
            od.OrderID,
            GROUP_CONCAT(i.Name SEPARATOR ', ') AS Items,
            GROUP_CONCAT(CONCAT(i.Name, ' (Qty: ', od.Quantity, ', Unit Price: ', od.UnitPrice, ')') SEPARATOR '\n') AS ItemDetails,
            SUM(od.TotalPrice) AS TotalAmount
        FROM 
            OrderDetails od
        JOIN 
            Orders o ON od.OrderID = o.OrderID
        JOIN 
            Item i ON od.ItemID = i.Item_id
        WHERE 
            o.Status = 'Completed' 
        GROUP BY 
            od.OrderID;
    """
    cur.execute(query_done)
    done_orders = cur.fetchall()

    for order in done_orders:
        done_tree.insert('', 'end', values=order)

    # Function to mark order as paid
    def mark_order_paid():
        selected = pending_tree.selection()
        if selected:
            for item in selected:
                order_id = pending_tree.item(item, "values")[0]
                total_amount = float(pending_tree.item(item, "values")[3])
                open_payment_window(order_id, total_amount)
                pending_tree.delete(item)
            refresh_done_orders()

    # Refresh done orders
    def refresh_done_orders():
        for row in done_tree.get_children():
            done_tree.delete(row)
        cur.execute(query_done)
        done_orders = cur.fetchall()
        for order in done_orders:
            done_tree.insert('', 'end', values=order)

    # Open payment window
    def open_payment_window(order_id, total_amount):
        payment_window = tk.Toplevel(root)
        payment_window.title("Payment")
        payment_window.geometry("500x300")
        payment_window.configure(bg="#e1f5fe")
        tk.Label(payment_window, text="Payment Window", font=("Helvetica", 14, "bold"), bg="#e1f5fe").pack(pady=10)

        tk.Label(payment_window, text=f"Total Amount Due: {total_amount}", font=("Helvetica", 12), bg="#e1f5fe").pack(pady=5)

        tk.Label(payment_window, text="Amount Paid:", bg="#e1f5fe").pack(pady=5)
        amount_entry = tk.Entry(payment_window)
        amount_entry.pack(pady=5)

        tk.Label(payment_window, text="Mode of Payment:", bg="#e1f5fe").pack(pady=5)
        mode_of_payment = tk.StringVar()
        ttk.Combobox(payment_window, textvariable=mode_of_payment, values=["Cash", "Credit Card", "Debit Card", "UPI", "Net Banking"]).pack(pady=5)

        tk.Button(payment_window, text="Confirm Payment", command=lambda: confirm_payment(order_id, total_amount, amount_entry.get(), mode_of_payment.get(), payment_window), bg="#2196f3", fg="white").pack(pady=10)

    # Function to handle payment confirmation
    def confirm_payment(order_id, total_amount, amount, mode, window):
        try:
            amount = float(amount)
            if amount < total_amount:
                messagebox.showerror("Payment Error", f"Amount paid ({amount}) is less than the total amount ({total_amount}).")
            else:
                change = amount - total_amount
                messagebox.showinfo("Payment Successful", f"Payment of {amount} confirmed. Change: {change:.2f}")
                cur.execute("UPDATE Orders SET Status = 'Completed' WHERE OrderID = %s", (order_id,))
                cur.execute("SELECT TableID FROM Orders WHERE OrderID = %s", (order_id,))
                table_id = cur.fetchone()
                if table_id:
                    # Mark the table as unoccupied
                    cur.execute("UPDATE `Tables` SET IsOccupied = FALSE WHERE Table_id = %s", (table_id[0],))
                con.commit()
                window.destroy()
                feedback_page(con, order_id)
        except ValueError:
            messagebox.showerror("Invalid Amount", "Please enter a valid numeric amount.")

    # Buttons for marking orders as paid
    button_frame = tk.Frame(pending_tab, bg="#f1f8e9")
    button_frame.pack(pady=10)
    tk.Button(button_frame, text="Mark as Paid & Pay", command=mark_order_paid, bg="#4caf50", fg="white", font=("Helvetica", 12)).pack()

    root.mainloop()
