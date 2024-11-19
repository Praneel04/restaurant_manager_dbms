import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from reservation import reservation_page  # Assuming you have this module

def show_reservations(con):
    root = tk.Toplevel()
    root.title("Reservations Management")
    
    root.configure(bg="#f4f4f4")

    # Fullscreen toggle functionality
    

    # Custom ttk Styles
    style = ttk.Style()
    style.theme_use('clam')  # Set a consistent theme
    style.configure("Treeview", background="#ffffff", foreground="#000000", rowheight=25, fieldbackground="#ffffff", font=("Helvetica", 12))
    style.configure("Treeview.Heading", font=("Helvetica", 14, "bold"))
    style.configure("Accent.TButton", font=("Helvetica", 12), padding=10, background="#2196f3", foreground="white")
    style.map("Accent.TButton", background=[("active", "#1e88e5")])

    ttk.Label(root, text="Reservation Management", font=("Helvetica", 20, "bold"), background="#f4f4f4").pack(pady=20)

    # Frame for displaying reservations
    reservations_frame = tk.Frame(root, bg="#e1f5fe", bd=2, relief="solid")
    reservations_frame.pack(fill="both", expand=True, padx=30, pady=20)

    # Treeview to display reservations
    tree = ttk.Treeview(reservations_frame, columns=("ReservationID", "TableID", "CustomerID", "Time", "NumberOfPeople"), show="headings")
    for col in ("ReservationID", "TableID", "CustomerID", "Time", "NumberOfPeople"):
        tree.heading(col, text=col, anchor="center")
        tree.column(col, anchor="center", width=120)
    tree.column("Time", anchor="center", width=250)
    tree.pack(fill="both", expand=True, padx=10, pady=10)

    # Fetch and display reservations
    cur = con.cursor()
    cur.execute("""
        SELECT Reservation_id, Table_id, Customer_id, Time, Number_of_people
        FROM Reservation
    """)
    reservations = cur.fetchall()

    for reservation in reservations:
        tree.insert('', 'end', values=reservation)

    # Function to mark a reservation as completed
    def complete_reservation():
        selected = tree.selection()
        if selected:
            for item in selected:
                reservation_id = tree.item(item, "values")[0]
                table_id = tree.item(item, "values")[1]

                # Remove the reservation
                cur.execute("DELETE FROM Reservation WHERE Reservation_id = %s", (reservation_id,))
                # Mark the table as unoccupied
                con.commit()
                tree.delete(item)
                messagebox.showinfo("Success", "Reservation completed successfully and table is now available.")
        else:
            messagebox.showwarning("Selection Error", "Please select a reservation to complete.")

    # Function to cancel a reservation
    def cancel_reservation():
        selected = tree.selection()
        if selected:
            for item in selected:
                reservation_id = tree.item(item, "values")[0]
                table_id = tree.item(item, "values")[1]

                # Remove the reservation
                cur.execute("DELETE FROM Reservation WHERE Reservation_id = %s", (reservation_id,))
                # Mark the table as unoccupied
                con.commit()
                tree.delete(item)
                messagebox.showinfo("Success", "Reservation cancelled successfully and table is now available.")
        else:
            messagebox.showwarning("Selection Error", "Please select a reservation to cancel.")

    # Buttons for actions
    button_frame = tk.Frame(root, bg="#f4f4f4")
    button_frame.pack(pady=20)

    ttk.Button(button_frame, text="Complete Reservation", command=complete_reservation, style="Accent.TButton").grid(row=0, column=0, padx=15)
    ttk.Button(button_frame, text="Cancel Reservation", command=cancel_reservation, style="Accent.TButton").grid(row=0, column=1, padx=15)
    ttk.Button(button_frame, text="Add New Reservation", command=lambda: reservation_page(con), style="Accent.TButton").grid(row=0, column=2, padx=15)

    root.mainloop()
