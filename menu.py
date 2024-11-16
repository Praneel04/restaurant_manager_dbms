import tkinter as tk
from tkinter import ttk, messagebox, StringVar, IntVar, Toplevel, Label, Entry, Button, Frame
def show_menu(con):
    root = Toplevel()
    root.title("Menu Management")
    
    # Display existing menu items
    tree = ttk.Treeview(root, columns=("item_id", "name", "price"), show="headings")
    tree.heading("item_id", text="Item ID")
    tree.heading("name", text="Name")
    tree.heading("price", text="Price")

    cur = con.cursor()
    cur.execute("SELECT Item_id, Name, Price FROM Item")
    menu_items = cur.fetchall()
    for item in menu_items:
        tree.insert('', 'end', values=item)
    tree.pack()

    # Add new menu item
    def add_item():
        name = menu_name_entry.get()
        price = menu_price_entry.get()
        if not name or not price:
            messagebox.showwarning("Input Error", "Please provide item name and price.")
            return
        
        cur = con.cursor()
        cur.execute("INSERT INTO Item (Name, Price) VALUES (%s, %s)", (name, price))
        con.commit()
        messagebox.showinfo('Success', "Item added!")
        menu_name_entry.delete(0, 'end')
        menu_price_entry.delete(0, 'end')
        tree.insert('', 'end', values=(cur.lastrowid, name, price))
        

    # Remove menu item
    def remove_item(con):
        selected = tree.focus()
        if selected:
            item_id = tree.item(selected)['values'][0]
            
            cur = con.cursor()
            cur.execute("DELETE FROM Item WHERE Item_id = %s", (item_id,))
            con.commit()
            tree.delete(selected)
            messagebox.showinfo('Success', "Item removed!")
    

    menu_name_entry = Entry(root)
    menu_name_entry.place(x=50, y=400)
    Label(root, text="Item Name").place(x=50, y=375)

    menu_price_entry = Entry(root)
    menu_price_entry.place(x=200, y=400)
    Label(root, text="Price").place(x=200, y=375)

    Button(root, text="Add Item", command=add_item).place(x=350, y=395)
    Button(root, text="Remove Item", command=remove_item).place(x=450, y=395)

    root.mainloop()