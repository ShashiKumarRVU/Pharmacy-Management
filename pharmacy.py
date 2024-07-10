import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import webbrowser


conn = sqlite3.connect('pharmacy.db')
cursor = conn.cursor()


cursor.execute('''
    CREATE TABLE IF NOT EXISTS medicines (
        id INTEGER PRIMARY KEY, 
        name TEXT, 
        price REAL, 
        quantity INTEGER, 
        expiry_date TEXT,
        location TEXT
    )
''')
conn.commit()

def add_medicine():
    name = name_entry.get()
    price = price_entry.get()
    quantity = quantity_entry.get()
    expiry_date = expiry_date_entry.get()
    location = location_entry.get()

    if name and price and quantity and expiry_date and location:
        cursor.execute("INSERT INTO medicines (name, price, quantity, expiry_date, location) VALUES (?, ?, ?, ?, ?)", (name, price, quantity, expiry_date, location))
        conn.commit()
        messagebox.showinfo("Success", "Medicine added successfully!")
        clear_entries()
    else:
        messagebox.showerror("Error", "Please enter all details.")

def update_medicine():
    name = name_entry.get()
    price = price_entry.get()
    quantity = quantity_entry.get()
    expiry_date = expiry_date_entry.get()
    location = location_entry.get()
 
    if name:
        cursor.execute("SELECT * FROM medicines WHERE name=?", (name,))
        medicine = cursor.fetchone()
        if medicine:
            cursor.execute("UPDATE medicines SET price=?, quantity=?, expiry_date=?, location=? WHERE name=?", (price, quantity, expiry_date, location, name))
            conn.commit()
            messagebox.showinfo("Success", "Medicine details updated successfully!")
            clear_entries()
        else:
            messagebox.showerror("Error", "Medicine not found!")
    else:
        messagebox.showerror("Error", "Please enter medicine name.")

def delete_medicine_window():
    delete_window = tk.Toplevel(root)
    delete_window.title("Delete Medicine")
    delete_window.geometry("300x100")

    delete_label = ttk.Label(delete_window, text="Enter Medicine Name:")
    delete_label.pack()

    delete_entry = ttk.Entry(delete_window)
    delete_entry.pack()

    delete_button = ttk.Button(delete_window, text="Delete", command=lambda: delete_medicine(delete_entry.get(), delete_window))
    delete_button.pack()

def delete_medicine(name, window):
    if name:
        cursor.execute("SELECT * FROM medicines WHERE name=?", (name,))
        medicine = cursor.fetchone()
        if medicine:
            cursor.execute("DELETE FROM medicines WHERE name=?", (name,))
            conn.commit()
            messagebox.showinfo("Success", "Medicine deleted successfully!")
            window.destroy()
            clear_entries()
        else:
            messagebox.showerror("Error", "Medicine not found!")
    else:
        messagebox.showerror("Error", "Please enter medicine name.")

def view_medicines():
    view_window = tk.Toplevel(root)
    view_window.title("Medicine List")
    view_window.geometry("300x200")
    scrollbar = ttk.Scrollbar(view_window)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    listbox = tk.Listbox(view_window, yscrollcommand=scrollbar.set)
    listbox.pack(expand=True, fill=tk.BOTH)

    cursor.execute("SELECT * FROM medicines")
    medicines = cursor.fetchall()
    if medicines:
        for medicine in medicines:
            listbox.insert(tk.END, f"Medicine: {medicine[1]}, Price: {medicine[2]}, Quantity: {medicine[3]}, Expiry Date: {medicine[4]}, Location: {medicine[5]}")
    else:
        listbox.insert(tk.END, "No medicines found!")

    scrollbar.config(command=listbox.yview)


def order_medicine_window():
    order_window = tk.Toplevel(root)
    order_window.title("Order Medicine")
    order_window.geometry("500x200")

    order_label = ttk.Label(order_window, text="Enter Medicine Name:")
    order_label.pack()

    order_entry = ttk.Entry(order_window)
    order_entry.pack()

    confirm_var = tk.StringVar(value="")
    confirm_label = ttk.Label(order_window, textvariable=confirm_var)
    confirm_label.pack()

    order_button = ttk.Button(order_window, text="Order", command=lambda: order_medicine(order_entry.get(), order_window, confirm_var))
    order_button.pack()

    order_window.mainloop()


def order_medicine(name, window, confirm_var):
    if name:
        cursor.execute("SELECT * FROM medicines WHERE name=?", (name ,))
        medicine = cursor.fetchone()
        if medicine:
            messagebox.showinfo("Order", f"{name} is available in stock! and order is confirmed")
            
        else:
            answer = messagebox.askquestion("Order", f"{name} is not available in stock. Do you want to order it from MedPlus?")
            if answer == "yes":
                webbrowser.open_new("https://www.medplusmart.com/")
                confirm_var.set("Order is confirmed")
            else:
                messagebox.showinfo("Order", "No problem, you can order it later.")
        window.destroy()
    else:
        messagebox.showerror("Error", "Please enter medicine name.")

def clear_entries():
    name_entry.delete(0, tk.END)
    price_entry.delete(0, tk.END)
    quantity_entry.delete(0, tk.END)
    expiry_date_entry.delete(0, tk.END)
    location_entry.delete(0, tk.END)


root = tk.Tk()
root.title("Pharmacy Management System")
root.geometry("500x400")


frame = tk.Frame(root, bg="lightgrey")
frame.place(relx=0.5, rely=0.5, anchor="center")



tk.Label(frame, text="Medicine Name:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
tk.Label(frame, text="Medicine Price:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
tk.Label(frame, text="Quantity:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
tk.Label(frame, text="Expiry Date:").grid(row=3, column=0, padx=5, pady=5, sticky="w")
tk.Label(frame, text="Location:").grid(row=4, column=0, padx=5, pady=5, sticky="w")


name_entry = ttk.Entry(frame)
name_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")
price_entry = ttk.Entry(frame)
price_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")
quantity_entry = ttk.Entry(frame)
quantity_entry.grid(row=2, column=1, padx=5, pady=5, sticky="w")
expiry_date_entry = ttk.Entry(frame)
expiry_date_entry.grid(row=3, column=1, padx=5, pady=5, sticky="w")
location_entry = ttk.Entry(frame)
location_entry.grid(row=4, column=1, padx=5, pady=5, sticky="w")




tk.Button(frame, text="Add Medicine", command=add_medicine).grid(row=8, column=1, padx=5, pady=5, sticky="w", anchor ="s")
tk.Button(frame, text="Update Medicine", command=update_medicine).grid(row=5, column=1, padx=5, pady=5, sticky="w")
tk.Button(frame, text="Delete Medicine", command=delete_medicine_window).grid(row=6, column=0, padx=5, pady=5, sticky="w")
tk.Button(frame, text="View Medicines", command=view_medicines).grid(row=6, column=1, padx=5, pady=5, sticky="w")

tk.Button(frame, text="Order Medicine", command=order_medicine_window).grid(row=7, column=0, padx=5, pady=5, sticky="ew")

root.mainloop()
