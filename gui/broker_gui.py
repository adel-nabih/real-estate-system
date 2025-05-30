import tkinter as tk
from tkinter import ttk, messagebox
from controllers.broker_controller import BrokerController
from models.broker import Broker

class BrokerGUI(tk.Frame):
    def __init__(self, parent, broker_controller: BrokerController):
        super().__init__(parent)
        self.controller = broker_controller
        
        # Create form frame
        self.form_frame = ttk.LabelFrame(self, text="Broker Details")
        self.form_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Create list frame
        self.list_frame = ttk.LabelFrame(self, text="Broker List")
        self.list_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Create treeview
        self.tree = ttk.Treeview(self.list_frame)
        self.tree.pack(fill=tk.BOTH, expand=True)
        
        # Configure treeview columns
        self.tree["columns"] = ("id", "name", "email", "phone", "commission_rate")
        self.tree.column("#0", width=0, stretch=tk.NO)
        self.tree.column("id", width=50)
        self.tree.column("name", width=200)
        self.tree.column("email", width=200)
        self.tree.column("phone", width=150)
        self.tree.column("commission_rate", width=100)
        
        self.tree.heading("id", text="ID")
        self.tree.heading("name", text="Name")
        self.tree.heading("email", text="Email")
        self.tree.heading("phone", text="Phone")
        self.tree.heading("commission_rate", text="Commission Rate")
        
        # Create form fields
        self.create_form_fields()
        
        # Create buttons
        self.create_buttons()
        
        # Load initial data
        self.refresh_data()
        
        # Bind treeview selection
        self.tree.bind("<<TreeviewSelect>>", self.on_select)

    def create_form_fields(self):
        """Create input fields for broker details."""
        # Name field
        ttk.Label(self.form_frame, text="Name:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.name_var = tk.StringVar()
        ttk.Entry(self.form_frame, textvariable=self.name_var).grid(row=0, column=1, sticky=(tk.W, tk.E), padx=5, pady=5)
        
        # Email field
        ttk.Label(self.form_frame, text="Email:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.email_var = tk.StringVar()
        ttk.Entry(self.form_frame, textvariable=self.email_var).grid(row=1, column=1, sticky=(tk.W, tk.E), padx=5, pady=5)
        
        # Phone field
        ttk.Label(self.form_frame, text="Phone:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        self.phone_var = tk.StringVar()
        ttk.Entry(self.form_frame, textvariable=self.phone_var).grid(row=2, column=1, sticky=(tk.W, tk.E), padx=5, pady=5)
        
        # Commission Rate field
        ttk.Label(self.form_frame, text="Commission Rate:").grid(row=3, column=0, sticky=tk.W, padx=5, pady=5)
        self.commission_rate_var = tk.StringVar()
        ttk.Entry(self.form_frame, textvariable=self.commission_rate_var).grid(row=3, column=1, sticky=(tk.W, tk.E), padx=5, pady=5)
        
        # Configure form frame grid
        self.form_frame.columnconfigure(1, weight=1)

    def create_buttons(self):
        """Create buttons for CRUD operations."""
        button_frame = ttk.Frame(self.form_frame)
        button_frame.grid(row=4, column=0, columnspan=2, pady=10)
        
        ttk.Button(button_frame, text="Add", command=self.add_item).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Update", command=self.update_item).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Delete", command=self.delete_item).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Clear", command=self.clear_form).pack(side=tk.LEFT, padx=5)

    def clear_form(self):
        """Clear all form fields."""
        self.name_var.set("")
        self.email_var.set("")
        self.phone_var.set("")
        self.commission_rate_var.set("")

    def on_select(self, event):
        """Handle treeview selection."""
        selected = self.tree.selection()
        if selected:
            item = self.tree.item(selected[0])
            values = item["values"]
            self.name_var.set(values[1])
            self.email_var.set(values[2])
            self.phone_var.set(values[3])
            self.commission_rate_var.set(values[4])

    def add_item(self):
        """Add a new broker."""
        try:
            name = self.name_var.get().strip()
            email = self.email_var.get().strip()
            phone = self.phone_var.get().strip()
            commission_rate = float(self.commission_rate_var.get().strip())
            
            if not all([name, email, phone]):
                messagebox.showerror("Error", "Name, email, and phone are required")
                return
                
            broker = Broker(
                name=name,
                email=email,
                phone=phone,
                commission_rate=commission_rate
            )
            self.controller.add(broker)
            messagebox.showinfo("Success", "Broker added successfully")
            self.clear_form()
            self.refresh_data()
            
        except ValueError as e:
            messagebox.showerror("Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def update_item(self):
        """Update selected broker."""
        selected = self.tree.selection()
        if not selected:
            messagebox.showerror("Error", "Please select a broker to update")
            return
            
        try:
            broker_id = self.tree.item(selected[0])["values"][0]
            name = self.name_var.get().strip()
            email = self.email_var.get().strip()
            phone = self.phone_var.get().strip()
            commission_rate = float(self.commission_rate_var.get().strip())
            
            if not all([name, email, phone]):
                messagebox.showerror("Error", "Name, email, and phone are required")
                return
                
            broker = Broker(
                id=broker_id,
                name=name,
                email=email,
                phone=phone,
                commission_rate=commission_rate
            )
            self.controller.update(broker)
            messagebox.showinfo("Success", "Broker updated successfully")
            self.refresh_data()
            
        except ValueError as e:
            messagebox.showerror("Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def delete_item(self):
        """Delete selected broker."""
        selected = self.tree.selection()
        if not selected:
            messagebox.showerror("Error", "Please select a broker to delete")
            return
            
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this broker?"):
            try:
                broker_id = self.tree.item(selected[0])["values"][0]
                self.controller.delete(broker_id)
                messagebox.showinfo("Success", "Broker deleted successfully")
                self.clear_form()
                self.refresh_data()
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def refresh_data(self):
        """Refresh the broker list."""
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        # Load and display brokers
        try:
            brokers = self.controller.get_all()
            for broker in brokers:
                self.tree.insert("", tk.END, values=(
                    broker.id,
                    broker.name,
                    broker.email,
                    broker.phone,
                    broker.commission_rate
                ))
        except Exception as e:
            messagebox.showerror("Error", f"Error loading brokers: {str(e)}") 