import tkinter as tk
from tkinter import ttk, messagebox
from controllers.property_controller import PropertyController
from models.property import Property

class PropertyGUI(tk.Frame):
    def __init__(self, parent, property_controller: PropertyController):
        super().__init__(parent)
        self.controller = property_controller
        
        self.style = ttk.Style()
        self.style.configure("Crud.TButton", background="#28a745", foreground="white", font=("Arial", 10, "bold"))

        self.form_frame = ttk.LabelFrame(self, text="Property Details", padding=10)
        self.form_frame.pack(fill=tk.X, padx=10, pady=10)

        self.list_frame = ttk.LabelFrame(self, text="Property List")
        self.list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.tree = ttk.Treeview(self.list_frame)
        self.tree.pack(fill=tk.BOTH, expand=True)
        
        self.tree["columns"] = ("id", "location", "type", "size", "price", "status")
        self.tree.column("#0", width=0, stretch=tk.NO)
        for col in self.tree["columns"]:
            self.tree.column(col, anchor=tk.CENTER, width=120)
            self.tree.heading(col, text=col.capitalize())
        
        self.create_form_fields()
        self.create_buttons()
        self.refresh_data()
        self.tree.bind("<<TreeviewSelect>>", self.on_select)

    def create_form_fields(self):
        ttk.Label(self.form_frame, text="Location:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.location_var = tk.StringVar()
        ttk.Entry(self.form_frame, textvariable=self.location_var).grid(row=0, column=1, sticky="ew", padx=5, pady=5)

        ttk.Label(self.form_frame, text="Type:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.type_var = tk.StringVar()
        ttk.Combobox(self.form_frame, textvariable=self.type_var, values=["House", "Apartment", "Commercial"]).grid(row=1, column=1, sticky="ew", padx=5, pady=5)

        ttk.Label(self.form_frame, text="Size (sqm):").grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        self.size_var = tk.StringVar()
        ttk.Entry(self.form_frame, textvariable=self.size_var).grid(row=2, column=1, sticky="ew", padx=5, pady=5)

        ttk.Label(self.form_frame, text="Price ($):").grid(row=3, column=0, sticky=tk.W, padx=5, pady=5)
        self.price_var = tk.StringVar()
        ttk.Entry(self.form_frame, textvariable=self.price_var).grid(row=3, column=1, sticky="ew", padx=5, pady=5)

        ttk.Label(self.form_frame, text="Status:").grid(row=4, column=0, sticky=tk.W, padx=5, pady=5)
        self.status_var = tk.StringVar()
        ttk.Combobox(self.form_frame, textvariable=self.status_var, values=["available", "sold"]).grid(row=4, column=1, sticky="ew", padx=5, pady=5)

        self.form_frame.columnconfigure(1, weight=1)

    def create_buttons(self):
        button_frame = ttk.Frame(self.form_frame)
        button_frame.grid(row=5, column=0, columnspan=2, pady=10)

        ttk.Button(button_frame, text="Add", style="Crud.TButton", command=self.add_item).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Update", style="Crud.TButton", command=self.update_item).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Delete", style="Crud.TButton", command=self.delete_item).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Clear", style="Crud.TButton", command=self.clear_form).pack(side=tk.LEFT, padx=5)

    def clear_form(self):
        self.location_var.set("")
        self.type_var.set("")
        self.size_var.set("")
        self.price_var.set("")
        self.status_var.set("")

    def on_select(self, event):
        selected = self.tree.selection()
        if selected:
            values = self.tree.item(selected[0])["values"]
            self.location_var.set(values[1])
            self.type_var.set(values[2])
            self.size_var.set(values[3])
            self.price_var.set(values[4])
            self.status_var.set(values[5])

    def add_item(self):
        try:
            location = self.location_var.get().strip()
            type_ = self.type_var.get().strip()
            size = int(self.size_var.get().strip())
            price = float(self.price_var.get().strip())
            status = self.status_var.get().strip()

            if not all([location, type_, status]):
                messagebox.showerror("Error", "Location, type, and status are required")
                return

            new_property = Property(location=location, type=type_, size=size, price=price, status=status)
            self.controller.add(new_property)
            self.refresh_data()
            self.clear_form()
            messagebox.showinfo("Success", "Property added successfully")

        except ValueError as e:
            messagebox.showerror("Invalid Input", str(e))

    def update_item(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showerror("Error", "Select a property to update")
            return

        try:
            property_id = self.tree.item(selected[0])["values"][0]
            location = self.location_var.get().strip()
            type_ = self.type_var.get().strip()
            size = int(self.size_var.get().strip())
            price = float(self.price_var.get().strip())
            status = self.status_var.get().strip()

            if not all([location, type_, status]):
                messagebox.showerror("Error", "All fields must be filled")
                return

            updated_property = Property(id=property_id, location=location, type=type_, size=size, price=price, status=status)
            self.controller.update(updated_property)
            self.refresh_data()
            messagebox.showinfo("Success", "Property updated successfully")

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def delete_item(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showerror("Error", "Select a property to delete")
            return
        try:
            property_id = self.tree.item(selected[0])["values"][0]
            self.controller.delete(property_id)
            self.refresh_data()
            messagebox.showinfo("Success", "Property deleted")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def refresh_data(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for prop in self.controller.get_all():
            self.tree.insert("", tk.END, values=(prop.id, prop.location, prop.type, prop.size, prop.price, prop.status))
