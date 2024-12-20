import tkinter as tk
from tkinter import ttk, messagebox

def show_staff(con):
    root = tk.Toplevel()
    root.title("Staff Management")
    root.geometry("1000x600")
    root.configure(bg="#f4f4f4")

    # Custom style for treeview
    style = ttk.Style()
    style.configure("Treeview", font=("Helvetica", 10), rowheight=25)
    style.configure("Treeview.Heading", font=("Helvetica", 12, "bold"))

    # Treeview to display staff
    staff_tree = ttk.Treeview(root, columns=("StaffID", "Name", "Email", "Phone", "StaffType", "Rating"), show="headings")
    for col in ("StaffID", "Name", "Email", "Phone", "StaffType", "Rating"):
        staff_tree.heading(col, text=col, anchor="center")
        staff_tree.column(col, anchor="center", width=150)
    staff_tree.column("StaffID", width=100)
    staff_tree.pack(fill="both", expand=True, padx=20, pady=20)

    # Fetch staff from the database
    cur = con.cursor()
    cur.execute("SELECT Staff_id, Name, Email, Phone, Staff_type, Rating FROM Staff")
    staff_members = cur.fetchall()

    for staff in staff_members:
        staff_tree.insert('', 'end', values=staff)

    # Function to add a new staff member
    def add_staff():
        name = name_entry.get().strip()
        email = email_entry.get().strip()
        phone = phone_entry.get().strip()
        staff_type = staff_type_entry.get().strip()
        rating = rating_entry.get().strip()

        if not name or not email or not staff_type:
            messagebox.showwarning("Input Error", "Please provide Name, Email, and Staff Type.")
            return

        try:
            rating = float(rating) if rating else None
            cur.execute("INSERT INTO Staff (Name, Email, Phone, Staff_type, Rating) VALUES (%s, %s, %s, %s, %s)", (name, email, phone, staff_type, rating))
            con.commit()
            staff_id = cur.lastrowid
            staff_tree.insert('', 'end', values=(staff_id, name, email, phone, staff_type, rating))
            messagebox.showinfo("Success", "Staff member added successfully!")
            name_entry.delete(0, 'end')
            email_entry.delete(0, 'end')
            phone_entry.delete(0, 'end')
            staff_type_entry.delete(0, 'end')
            rating_entry.delete(0, 'end')
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    # Function to remove a selected staff member
    def remove_staff():
        selected = staff_tree.selection()
        if not selected:
            messagebox.showwarning("Selection Error", "Please select a staff member to remove.")
            return

        confirm = messagebox.askyesno("Confirm Deletion", "Are you sure you want to remove the selected staff member?")
        if confirm:
            for item in selected:
                staff_id = staff_tree.item(item, "values")[0]
                try:
                    cur.execute("DELETE FROM Staff WHERE Staff_id = %s", (staff_id,))
                    con.commit()
                    staff_tree.delete(item)
                    messagebox.showinfo("Success", "Staff member removed successfully!")
                except Exception as e:
                    messagebox.showerror("Error", f"An error occurred: {e}")

    # Frame for adding new staff
    add_frame = tk.Frame(root, bg="#e1f5fe", padx=10, pady=10)
    add_frame.pack(pady=10)

    tk.Label(add_frame, text="Name:", bg="#e1f5fe").grid(row=0, column=0, padx=5, pady=5)
    name_entry = tk.Entry(add_frame)
    name_entry.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(add_frame, text="Email:", bg="#e1f5fe").grid(row=0, column=2, padx=5, pady=5)
    email_entry = tk.Entry(add_frame)
    email_entry.grid(row=0, column=3, padx=5, pady=5)

    tk.Label(add_frame, text="Phone:", bg="#e1f5fe").grid(row=0, column=4, padx=5, pady=5)
    phone_entry = tk.Entry(add_frame)
    phone_entry.grid(row=0, column=5, padx=5, pady=5)

    tk.Label(add_frame, text="Staff Type:", bg="#e1f5fe").grid(row=1, column=0, padx=5, pady=5)
    staff_type_entry = tk.Entry(add_frame)
    staff_type_entry.grid(row=1, column=1, padx=5, pady=5)

    tk.Label(add_frame, text="Rating:", bg="#e1f5fe").grid(row=1, column=2, padx=5, pady=5)
    rating_entry = tk.Entry(add_frame)
    rating_entry.grid(row=1, column=3, padx=5, pady=5)

    tk.Button(add_frame, text="Add Staff", command=add_staff, bg="#4caf50", fg="white").grid(row=1, column=4, padx=10, pady=5)

    # Button for removing a staff member
    tk.Button(root, text="Remove Selected Staff", command=remove_staff, bg="#f44336", fg="white").pack(pady=10)

    root.mainloop()
