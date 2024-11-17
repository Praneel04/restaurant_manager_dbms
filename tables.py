import tkinter as tk
from tkinter import ttk, messagebox

def show_tables(con):
    root = tk.Toplevel()
    root.title("Tables Management")
    root.geometry("800x500")

    # Frame for table list
    table_frame = tk.Frame(root)
    table_frame.pack(pady=20, padx=20, fill="both", expand=True)

    # Treeview for displaying tables
    columns = ("TableID", "TotalPeople", "IsOccupied", "TableType")
    tree = ttk.Treeview(table_frame, columns=columns, show="headings")
    for col in columns:
        tree.heading(col, text=col, anchor="center")
        tree.column(col, anchor="center", width=100 if col != "TableType" else 150)

    tree.pack(fill="both", expand=True, padx=10, pady=10)

    # Fetch and display tables from the database
    cur = con.cursor()
    cur.execute("SELECT Table_id, Total_people, IsOccupied, TableType FROM `Tables`")
    tables = cur.fetchall()
    for table in tables:
        tree.insert('', 'end', values=table)

    # Add Table Frame
    add_frame = tk.Frame(root)
    add_frame.pack(pady=10)

    tk.Label(add_frame, text="Total People:").grid(row=0, column=0, padx=5, pady=5)
    total_people_entry = tk.Entry(add_frame, width=10)
    total_people_entry.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(add_frame, text="Table Type:").grid(row=0, column=2, padx=5, pady=5)
    table_type_entry = tk.Entry(add_frame, width=15)
    table_type_entry.grid(row=0, column=3, padx=5, pady=5)

    def add_table():
        total_people = total_people_entry.get().strip()
        table_type = table_type_entry.get().strip()

        if not total_people or not table_type:
            messagebox.showwarning("Input Error", "Please provide all required details.")
            return

        try:
            total_people = int(total_people)
            cur = con.cursor()
            cur.execute("INSERT INTO `Tables` (Total_people, IsOccupied, TableType) VALUES (%s, FALSE, %s)", (total_people, table_type))
            con.commit()

            # Insert the new table into the treeview
            new_table_id = cur.lastrowid
            tree.insert('', 'end', values=(new_table_id, total_people, 0, table_type))

            messagebox.showinfo("Success", "Table added successfully.")
            total_people_entry.delete(0, 'end')
            table_type_entry.delete(0, 'end')
        except ValueError:
            messagebox.showerror("Input Error", "Please enter a valid integer for total people.")

    tk.Button(add_frame, text="Add Table", command=add_table, bg="#4caf50", fg="white").grid(row=0, column=4, padx=10, pady=5)

    # Remove Table Function
    def remove_table():
        selected = tree.focus()
        if selected:
            table_id = tree.item(selected)['values'][0]
            try:
                cur = con.cursor()
                cur.execute("DELETE FROM `Tables` WHERE Table_id = %s", (table_id,))
                con.commit()
                tree.delete(selected)

                messagebox.showinfo("Success", "Table removed successfully.")
            except Exception as e:
                messagebox.showerror("Error", f"Could not remove the table. Error: {e}")
        else:
            messagebox.showwarning("Selection Error", "Please select a table to remove.")

    # Remove Table Button
    tk.Button(root, text="Remove Table", command=remove_table, bg="#f44336", fg="white").pack(pady=10)

    root.mainloop()
