import tkinter as tk
from tkinter import ttk, messagebox, StringVar, IntVar, Toplevel, Label, Entry, Button, Frame
def manage_users(con):
    user_root = tk.Toplevel()
    user_root.title("User Management")
    user_root.geometry("500x400")
    user_root.configure(bg="#f4f4f4")

    ttk.Label(user_root, text="User Management", font=("Helvetica", 16, "bold")).pack(pady=20)

    # Entry fields for creating a new user
    ttk.Label(user_root, text="New Username:").pack(pady=5)
    new_username = tk.StringVar()
    username_entry = ttk.Entry(user_root, textvariable=new_username)
    username_entry.pack(pady=5)

    ttk.Label(user_root, text="New Password:").pack(pady=5)
    new_password = tk.StringVar()
    password_entry = ttk.Entry(user_root, textvariable=new_password, show="*")
    password_entry.pack(pady=5)

    # Function to add a new user
    def add_user():
        username = new_username.get().strip()
        password = new_password.get().strip()
        if not username or not password:
            messagebox.showwarning("Input Error", "Please enter both a username and password.")
            return

        
        cur = con.cursor()
        cur.execute("SELECT * FROM admin WHERE username = %s", (username,))
        existing_user = cur.fetchone()
        if existing_user:
            messagebox.showwarning("User Exists", "This username already exists. Please choose a different username.")
        else:
            cur.execute("INSERT INTO admin (username, password) VALUES (%s, %s)", (username, password))
            con.commit()
            messagebox.showinfo("Success", "New user added successfully.")
            username_entry.delete(0, 'end')
            password_entry.delete(0, 'end')
        
    # Button to add user
    ttk.Button(user_root, text="Add User", command=add_user).pack(pady=20)

    # Display existing users
    ttk.Label(user_root, text="Existing Users:", font=("Helvetica", 12, "bold")).pack(pady=10)
    user_list_frame = tk.Frame(user_root)
    user_list_frame.pack(pady=10)

    tree = ttk.Treeview(user_list_frame, columns=("Username",), show="headings")
    tree.heading("Username", text="Username")
    tree.column("Username", anchor="center", width=200)
    tree.pack()

    # Fetch and display existing users
    def load_users():
        for row in tree.get_children():
            tree.delete(row)
        cur = con.cursor()
        cur.execute("SELECT username FROM admin")
        for row in cur.fetchall():
            tree.insert('', 'end', values=row)

    load_users()

    user_root.mainloop()
