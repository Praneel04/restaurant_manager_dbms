import tkinter as tk
from tkinter import ttk, messagebox, Toplevel, Label, Entry, Button

def show_menu(con):
    root = Toplevel()
    root.title("Menu Management")
    root.geometry("600x500")
    root.configure(bg="#f5f5f5")  # Light background color
    
    # Style Configuration
    style = ttk.Style()
    style.configure("Treeview", background="#e0f7fa", foreground="black", rowheight=25, fieldbackground="#e0f7fa")
    style.map("Treeview", background=[("selected", "#80deea")])
    
    # Display existing menu items
    tree = ttk.Treeview(root, columns=("item_id", "name", "price"), show="headings", height=12)
    tree.heading("item_id", text="Item ID")
    tree.heading("name", text="Name")
    tree.heading("price", text="Price")
    
    tree.column("item_id", width=100, anchor="center")
    tree.column("name", width=200, anchor="w")
    tree.column("price", width=100, anchor="e")
    tree.place(x=30, y=20)

    # Fetch and display items from the database
    cur = con.cursor()
    cur.execute("SELECT Item_id, Name, Price FROM Item")
    menu_items = cur.fetchall()
    for item in menu_items:
        tree.insert('', 'end', values=item)

    # Add item frame
    add_frame = tk.Frame(root, bg="#fafafa", bd=2, relief="solid")
    add_frame.place(x=30, y=380, width=550, height=90)
    
    Label(add_frame, text="Item Name:", bg="#fafafa", font=("Helvetica", 10)).place(x=10, y=15)
    menu_name_entry = Entry(add_frame, width=20, font=("Helvetica", 10))
    menu_name_entry.place(x=100, y=15)

    Label(add_frame, text="Price:", bg="#fafafa", font=("Helvetica", 10)).place(x=290, y=15)
    menu_price_entry = Entry(add_frame, width=10, font=("Helvetica", 10))
    menu_price_entry.place(x=340, y=15)

    def add_item():
        name = menu_name_entry.get()
        price = menu_price_entry.get()
        if not name or not price:
            messagebox.showwarning("Input Error", "Please provide item name and price.")
            return
        
        try:
            float(price)  # Validate price is numeric
        except ValueError:
            messagebox.showerror("Input Error", "Price must be a numeric value.")
            return

        
        cur = con.cursor()
            # Call the stored procedure
        cur.callproc('AddMenuItem', [name, price])
        con.commit()
        messagebox.showinfo('Success', "Item added!")
        menu_name_entry.delete(0, 'end')
        menu_price_entry.delete(0, 'end')

            # Fetch the last inserted item to update the UI
        cur.execute("SELECT LAST_INSERT_ID()")
        item_id = cur.fetchone()[0]
        tree.insert('', 'end', values=(item_id, name, price))
    
        
    Button(add_frame, text="Add Item", command=add_item, bg="#4caf50", fg="white", font=("Helvetica", 10), width=12).place(x=100, y=50)

    def remove_item():
        selected = tree.focus()
        if selected:
            item_id = tree.item(selected)['values'][0]
            
            cur = con.cursor()
                # Call the stored procedure
            cur.callproc('RemoveMenuItem', [item_id])
            con.commit()
            tree.delete(selected)
            messagebox.showinfo('Success', "Item removed!")
            
        else:
            messagebox.showwarning("Selection Error", "Please select an item to remove.")
            
    Button(add_frame, text="Remove Item", command=remove_item, bg="#f44336", fg="white", font=("Helvetica", 10), width=12).place(x=240, y=50)

    root.mainloop()
