import tkinter as tk
from tkinter import ttk, messagebox, StringVar, IntVar, Toplevel, Label, Entry, Button, Frame
def show_feedback(con):
    root = Toplevel()
    root.title("Customer Feedback")

    tree = ttk.Treeview(root, columns=("feedback_id", "customer_name", "staff_name", "item_name", "staff_rating", "item_rating", "feedback_text"), show="headings")
    tree.heading("feedback_id", text="Feedback ID")
    tree.heading("customer_name", text="Customer Name")
    tree.heading("staff_name", text="Staff Name")
    tree.heading("item_name", text="Item Name")
    tree.heading("staff_rating", text="Staff Rating")
    tree.heading("item_rating", text="Item Rating")
    tree.heading("feedback_text", text="Feedback")
    tree.pack()

    def refresh_feedback():
        for row in tree.get_children():
            tree.delete(row)
        cur = con.cursor()
        query = """
            SELECT 
                f.Feedback_id,
                c.Name AS customer_name,
                s.Name AS staff_name,
                i.Name AS item_name,
                f.Staff_rating,
                f.Item_rating,
                f.Feedback_text
            FROM Feedback f
            JOIN Customer c ON f.Customer_id = c.Customer_id
            JOIN Staff s ON f.Staff_id = s.Staff_id
            JOIN Item i ON f.Item_id = i.Item_id
        """
        cur.execute(query)
        feedbacks = cur.fetchall()
        for feedback in feedbacks:
            tree.insert('', 'end', values=feedback)

    Button(root, text="Refresh Feedback", command=refresh_feedback).place(x=250, y=400)
    refresh_feedback()

    root.mainloop()