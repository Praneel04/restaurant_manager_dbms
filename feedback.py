import tkinter as tk
from tkinter import ttk, messagebox

def feedback_page(con, order_id):
    root = tk.Toplevel()
    root.title("Feedback")
    root.geometry("500x400")

    # Fetch the staff assigned to the order
    cur = con.cursor()
    cur.execute("SELECT StaffID FROM Orders WHERE OrderID = %s", (order_id,))
    staff_result = cur.fetchone()
    if staff_result and staff_result[0]:
        staff_id = staff_result[0]
    else:
        messagebox.showerror("Error", "No staff assigned to this order.")
        root.destroy()
        return

    tk.Label(root, text="Thank you for your payment!", font=("Helvetica", 14, "bold")).pack(pady=10)
    tk.Label(root, text="We value your feedback.", font=("Helvetica", 12)).pack(pady=5)

    tk.Label(root, text="Rate your experience (1-5):").pack(pady=5)
    rating_var = tk.IntVar(value=0)

    # Display the rating dynamically
    rating_display = tk.Label(root, text="Selected Rating: 0")
    rating_display.pack(pady=5)

    def update_rating_display(event):
        rating_display.config(text=f"Selected Rating: {rating_var.get()}")

    rating_scale = ttk.Scale(root, from_=1, to=5, variable=rating_var, orient='horizontal', command=update_rating_display)
    rating_scale.pack(pady=5)

    tk.Label(root, text=f"Staff Assigned (ID: {staff_id}):", font=("Helvetica", 10)).pack(pady=5)

    tk.Label(root, text="Additional Comments:").pack(pady=5)
    comments_text = tk.Text(root, height=5, width=40)
    comments_text.pack(pady=5)

    def submit_feedback():
        rating = rating_var.get()
        comments = comments_text.get("1.0", tk.END).strip()

        if rating < 1 or rating > 5:
            messagebox.showwarning("Input Error", "Please provide a rating between 1 and 5.")
            return

        # Update the staff member's rating
        try:
            cur = con.cursor()
            cur.execute("SELECT Rating FROM Staff WHERE Staff_id = %s", (staff_id,))
            result = cur.fetchone()
            if result:
                current_rating = result[0] if result[0] is not None else 0
                # Simple average calculation for demonstration; adjust as needed
                new_rating = (current_rating + rating) / 2
                cur.execute("UPDATE Staff SET Rating = %s WHERE Staff_id = %s", (new_rating, staff_id))
                con.commit()
                messagebox.showinfo("Thank You", "Your feedback has been submitted, and the staff rating has been updated.")
            else:
                messagebox.showwarning("Invalid Staff ID", "No staff member found with the provided Staff ID.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

        # Optionally, you could log the feedback in another table if needed
        root.destroy()

    tk.Button(root, text="Submit Feedback", command=submit_feedback, bg="#4caf50", fg="white", font=("Helvetica", 12)).pack(pady=10)

    root.mainloop()
