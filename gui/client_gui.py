import tkinter as tk
from tkinter import ttk, messagebox
from controllers.client_controller import ClientController
from models.client import Client

class ClientGUI(tk.Frame):
    def __init__(self, parent, client_controller: ClientController):
        super().__init__(parent)
        self.controller = client_controller
        
        # Create form frame
        self.form_frame = ttk.LabelFrame(self, text="Client Details")
        self.form_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Create list frame
        self.list_frame = ttk.LabelFrame(self, text="Client List")
        self.list_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Create treeview
        self.tree = ttk.Treeview(self.list_frame)
        self.tree.pack(fill=tk.BOTH, expand=True)
        
        # Configure treeview columns
        self.tree["columns"] = ("id", "name", "contact", "preferences", "broker_id")
        self.tree.column("#0", width=0, stretch=tk.NO)
        self.tree.column("id", width=50)
        self.tree.column("name", width=200)
        self.tree.column("contact", width=200)
        self.tree.column("preferences", width=200)
        self.tree.column("broker_id", width=100)
        
        self.tree.heading("id", text="ID")
        self.tree.heading("name", text="Name")
        self.tree.heading("contact", text="Contact")
        self.tree.heading("preferences", text="Preferences")
        self.tree.heading("broker_id", text="Broker ID")
        
        # Create form fields
        self.create_form_fields()
        
        # Create buttons
        self.create_buttons()
        
        # Load initial data
        self.refresh_data()
        
        # Bind treeview selection
        self.tree.bind("<<TreeviewSelect>>", self.on_select)

    def create_form_fields(self):
        """Create input fields for client details."""
        # Name field
        ttk.Label(self.form_frame, text="Name:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.name_var = tk.StringVar()
        ttk.Entry(self.form_frame, textvariable=self.name_var).grid(row=0, column=1, sticky=(tk.W, tk.E), padx=5, pady=5)
        
        # Contact field
        ttk.Label(self.form_frame, text="Contact:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.contact_var = tk.StringVar()
        ttk.Entry(self.form_frame, textvariable=self.contact_var).grid(row=1, column=1, sticky=(tk.W, tk.E), padx=5, pady=5)
        
        # Preferences field
        ttk.Label(self.form_frame, text="Preferences:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        self.preferences_var = tk.StringVar()
        ttk.Entry(self.form_frame, textvariable=self.preferences_var).grid(row=2, column=1, sticky=(tk.W, tk.E), padx=5, pady=5)
        
        # Broker ID field
        ttk.Label(self.form_frame, text="Broker ID:").grid(row=3, column=0, sticky=tk.W, padx=5, pady=5)
        self.broker_id_var = tk.StringVar()
        ttk.Entry(self.form_frame, textvariable=self.broker_id_var).grid(row=3, column=1, sticky=(tk.W, tk.E), padx=5, pady=5)
        
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
        self.contact_var.set("")
        self.preferences_var.set("")
        self.broker_id_var.set("")

    def on_select(self, event):
        """Handle treeview selection."""
        selected = self.tree.selection()
        if selected:
            item = self.tree.item(selected[0])
            values = item["values"]
            self.name_var.set(values[1])
            self.contact_var.set(values[2])
            self.preferences_var.set(values[3])
            self.broker_id_var.set(values[4] if values[4] else "")

    def add_item(self):
        """Add a new client."""
        try:
            name = self.name_var.get().strip()
            contact = self.contact_var.get().strip()
            preferences = self.preferences_var.get().strip()
            broker_id = self.broker_id_var.get().strip()
            
            if not name:
                messagebox.showerror("Error", "Name is required")
                return
                
            client = Client(
                name=name,
                contact=contact,
                preferences=preferences,
                broker_id=int(broker_id) if broker_id else None
            )
            self.controller.add(client)
            messagebox.showinfo("Success", "Client added successfully")
            self.clear_form()
            self.refresh_data()
            
        except ValueError as e:
            messagebox.showerror("Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def update_item(self):
        """Update selected client."""
        selected = self.tree.selection()
        if not selected:
            messagebox.showerror("Error", "Please select a client to update")
            return
            
        try:
            client_id = self.tree.item(selected[0])["values"][0]
            name = self.name_var.get().strip()
            contact = self.contact_var.get().strip()
            preferences = self.preferences_var.get().strip()
            broker_id = self.broker_id_var.get().strip()
            
            if not name:
                messagebox.showerror("Error", "Name is required")
                return
                
            client = Client(
                id=client_id,
                name=name,
                contact=contact,
                preferences=preferences,
                broker_id=int(broker_id) if broker_id else None
            )
            self.controller.update(client)
            messagebox.showinfo("Success", "Client updated successfully")
            self.refresh_data()
            
        except ValueError as e:
            messagebox.showerror("Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def delete_item(self):
        """Delete selected client."""
        selected = self.tree.selection()
        if not selected:
            messagebox.showerror("Error", "Please select a client to delete")
            return
            
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this client?"):
            try:
                client_id = self.tree.item(selected[0])["values"][0]
                self.controller.delete(client_id)
                messagebox.showinfo("Success", "Client deleted successfully")
                self.clear_form()
                self.refresh_data()
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def refresh_data(self):
        """Refresh the client list."""
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        # Load and display clients
        try:
            clients = self.controller.get_all()
            for client in clients:
                self.tree.insert("", tk.END, values=(
                    client.id,
                    client.name,
                    client.contact,
                    client.preferences,
                    client.broker_id
                ))
        except Exception as e:
            messagebox.showerror("Error", f"Error loading clients: {str(e)}") 