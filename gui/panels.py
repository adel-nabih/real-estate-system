import tkinter as tk
from tkinter import ttk, messagebox
from decimal import Decimal 
import datetime 

# Import all models
from models.client import Client
from models.broker import Broker
from models.property import Property 
from models.sale import Sale

# Import all controllers, including get_by_id functions for pre-checks and new broker-specific filters
from controllers.client_controller import get_all_clients, add_client, update_client, delete_client, get_client_by_id, get_clients_by_broker_id
from controllers.broker_controller import get_all_brokers, add_broker, update_broker, delete_broker, get_broker_by_id
from controllers.property_controller import get_all_properties, add_property, update_property, delete_property, get_property_by_id
from controllers.sale_controller import get_all_sales, add_sale, update_sale, delete_sale, get_sales_by_broker_id, get_sale_by_id # get_sale_by_id is needed for broker sale permissions

class BasePanel(ttk.Frame):
    def __init__(self, parent, role, user_id): # Added role and user_id
        super().__init__(parent)
        self.role = role
        self.user_id = user_id # This will be broker_id for broker, client_id for client, None for admin
        self.setup_ui()
    
    @classmethod
    def setup_styles(cls):
        """Configures custom ttk styles for buttons.
        This is a classmethod and should be called once at application startup.
        """
        style = ttk.Style()

        # General TButton style (for login buttons and any unstyled ttk.Button)
        style.configure("TButton", 
                        background="#E0E0E0", # Light grey default
                        foreground="black", # Ensure black text on light buttons
                        font=("Arial", 10))
        style.map("TButton",
                  background=[("active", "#B0B0B0")], # Darker grey on hover
                  foreground=[("active", "black"), ("disabled", "gray")]) 

        # Login Buttons (distinct style for main page buttons)
        style.configure("Login.TButton",
                        background="#007BFF", # A nice blue
                        foreground="white",
                        font=("Arial", 12, "bold"),
                        padding=10,
                        relief="raised",
                        bordercolor="#0056b3",
                        borderwidth=2)
        style.map("Login.TButton",
                  background=[("active", "#0056b3")],
                  foreground=[("active", "white")])

        # Define custom button styles for panels
        # Add Button (Green)
        style.configure("Add.TButton", 
                        background="#4CAF50", # Green
                        foreground="white",
                        font=("Arial", 10, "bold"),
                        padding=5,
                        relief="raised",
                        bordercolor="#388E3C",
                        borderwidth=2,
                        focusthickness=1,
                        focuscolor="none")
        style.map("Add.TButton", 
                  background=[("active", "#66BB6A")],
                  foreground=[("active", "white")]) 

        # Update Button (Orange/Yellow)
        style.configure("Update.TButton", 
                        background="#FFC107", # Amber/Yellow
                        foreground="black", # Explicitly black text for visibility on light background
                        font=("Arial", 10, "bold"),
                        padding=5,
                        relief="raised",
                        bordercolor="#FFA000",
                        borderwidth=2,
                        focusthickness=1,
                        focuscolor="none")
        style.map("Update.TButton", 
                  background=[("active", "#FFD54F")],
                  foreground=[("active", "black")]) # Ensure text stays black on hover

        # Delete Button (Red)
        style.configure("Delete.TButton", 
                        background="#F44336", # Red
                        foreground="white",
                        font=("Arial", 10, "bold"),
                        padding=5,
                        relief="raised",
                        bordercolor="#D32F2F",
                        borderwidth=2,
                        focusthickness=1,
                        focuscolor="none")
        style.map("Delete.TButton", 
                  background=[("active", "#EF5350")],
                  foreground=[("active", "white")]) 

        # Refresh Button (Blue)
        style.configure("Refresh.TButton", 
                        background="#2196F3", # Blue
                        foreground="white",
                        font=("Arial", 10, "bold"),
                        padding=5,
                        relief="raised",
                        bordercolor="#1976D2",
                        borderwidth=2,
                        focusthickness=1,
                        focuscolor="none")
        style.map("Refresh.TButton", 
                  background=[("active", "#42A5F5")],
                  foreground=[("active", "white")]) 
        
        # Style for Labels to ensure dark text
        style.configure("TLabel", foreground="black")


    def setup_ui(self):
        # Create main container
        self.main_frame = ttk.Frame(self)
        self.main_frame.pack(expand=True, fill="both", padx=10, pady=10)
        
        # Create table
        self.create_table()
        
        # Create buttons frame
        self.create_buttons()
        
        # Create form frame
        self.create_form()
        
        # Load initial data
        self.refresh_data()

        # Bind treeview selection event (implemented in subclasses)
        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)
    
    def create_table(self):
        # Create treeview with scrollbar
        self.tree_frame = ttk.Frame(self.main_frame)
        self.tree_frame.pack(expand=True, fill="both", pady=(0, 10))
        
        self.tree_scroll = ttk.Scrollbar(self.tree_frame)
        self.tree_scroll.pack(side="right", fill="y")
        
        self.tree = ttk.Treeview(self.tree_frame, yscrollcommand=self.tree_scroll.set)
        self.tree.pack(expand=True, fill="both")
        
        self.tree_scroll.config(command=self.tree.yview)
    
    def create_buttons(self):
        self.button_frame = ttk.Frame(self.main_frame)
        self.button_frame.pack(fill="x", pady=(0, 10))
        
        self.add_btn = ttk.Button(
            self.button_frame,
            text="Add",
            command=self.add_item,
            style="Add.TButton" 
        )
        self.add_btn.pack(side="left", padx=5)
        
        self.update_btn = ttk.Button(
            self.button_frame,
            text="Update",
            command=self.update_item,
            style="Update.TButton" 
        )
        self.update_btn.pack(side="left", padx=5)
        
        self.delete_btn = ttk.Button(
            self.button_frame,
            text="Delete",
            command=self.delete_item,
            style="Delete.TButton" 
        )
        self.delete_btn.pack(side="left", padx=5)
        
        self.refresh_btn = ttk.Button(
            self.button_frame,
            text="Refresh",
            command=self.refresh_data,
            style="Refresh.TButton" 
        )
        self.refresh_btn.pack(side="right", padx=5)

        # --- Role-based Button Permissions ---
        # Clients cannot perform any CRUD operations on any panel
        if self.role == "Client":
            self.add_btn.config(state="disabled")
            self.update_btn.config(state="disabled")
            self.delete_btn.config(state="disabled")
        # Brokers and Admins have full CRUD by default on their respective panels
        # Specific panels (ClientPanel, SalePanel) will have additional checks for Broker role
        # to restrict actions to their own data.

    def create_form(self):
        self.form_frame = ttk.LabelFrame(self.main_frame, text="Details")
        self.form_frame.pack(fill="x", pady=(0, 10))
    
    def refresh_data(self):
        pass
    
    def add_item(self):
        pass
    
    def update_item(self):
        pass
    
    def delete_item(self):
        pass

    def on_tree_select(self, event):
        """
        Generic method to handle treeview selection.
        Subclasses should override this to populate their specific form fields.
        """
        selected_item = self.tree.focus()
        if selected_item:
            values = self.tree.item(selected_item, "values")
            self._populate_form_fields(values)
        else: # If nothing is selected (e.g., user clicks off a row)
            self.clear_form()


    def _populate_form_fields(self, values):
        """
        Internal helper method to populate form fields.
        Must be overridden by subclasses.
        """
        raise NotImplementedError("Subclasses must implement _populate_form_fields method.")

class ClientPanel(BasePanel):
    def __init__(self, parent, role, user_id):
        super().__init__(parent, role, user_id)
        self.setup_client_ui()
        # For Broker role, ensure broker_id field is pre-filled and potentially read-only
        if self.role == "Broker":
            self.broker_id_var.set(str(self.user_id))
            # self.broker_id_entry.config(state="readonly") # Uncomment if you have an entry reference

    def setup_client_ui(self):
        self.tree["columns"] = ("id", "name", "contact", "preferences", "broker_id")
        self.tree.column("#0", width=0, stretch="no")
        self.tree.column("id", width=50)
        self.tree.column("name", width=150)
        self.tree.column("contact", width=150)
        self.tree.column("preferences", width=200)
        self.tree.column("broker_id", width=100)
        
        self.tree.heading("id", text="ID")
        self.tree.heading("name", text="Name")
        self.tree.heading("contact", text="Contact")
        self.tree.heading("preferences", text="Preferences")
        self.tree.heading("broker_id", text="Broker ID")
        
        self.create_form_fields()
    
    def create_form_fields(self):
        ttk.Label(self.form_frame, text="Name:").grid(row=0, column=0, padx=5, pady=5)
        self.name_var = tk.StringVar()
        ttk.Entry(self.form_frame, textvariable=self.name_var).grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(self.form_frame, text="Contact:").grid(row=0, column=2, padx=5, pady=5)
        self.contact_var = tk.StringVar()
        ttk.Entry(self.form_frame, textvariable=self.contact_var).grid(row=0, column=3, padx=5, pady=5)
        
        ttk.Label(self.form_frame, text="Preferences:").grid(row=1, column=0, padx=5, pady=5)
        self.preferences_var = tk.StringVar()
        ttk.Entry(self.form_frame, textvariable=self.preferences_var).grid(row=1, column=1, columnspan=3, sticky="ew", padx=5, pady=5)
        
        ttk.Label(self.form_frame, text="Broker ID:").grid(row=2, column=0, padx=5, pady=5)
        self.broker_id_var = tk.StringVar()
        # Store the entry widget reference to potentially disable it later
        self.broker_id_entry = ttk.Entry(self.form_frame, textvariable=self.broker_id_var)
        self.broker_id_entry.grid(row=2, column=1, padx=5, pady=5)
        
        # Disable broker_id entry for brokers
        if self.role == "Broker":
            self.broker_id_entry.config(state="readonly")


    def refresh_data(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        if self.role == "Broker":
            # Broker sees only their clients
            clients = get_clients_by_broker_id(self.user_id) # Use the broker's ID
        else:
            # Admin sees all clients (Client role won't see this tab)
            clients = get_all_clients() 
            
        for client in clients:
            self.tree.insert("", "end", values=(
                client.id,
                client.name,
                client.contact,
                client.preferences,
                client.broker_id
            ))
    
    def add_item(self):
        try:
            # If broker, auto-assign their ID and ensure it's not changed
            broker_id_for_new_client = int(self.broker_id_var.get()) if self.broker_id_var.get() else None
            if self.role == "Broker":
                broker_id_for_new_client = self.user_id # Force broker_id to logged-in broker's ID

            new_client = Client(
                id=None, 
                name=self.name_var.get(),
                contact=self.contact_var.get(),
                preferences=self.preferences_var.get(),
                broker_id=broker_id_for_new_client
            )
            add_client(new_client) 
            self.refresh_data()
            self.clear_form()
            messagebox.showinfo("Success", "Client added successfully!")
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def update_item(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a client to update")
            return
        
        try:
            client_id = self.tree.item(selected[0])["values"][0]
            
            # If broker, ensure they can only update their own clients
            if self.role == "Broker":
                existing_client = get_client_by_id(client_id)
                if existing_client and existing_client.broker_id != self.user_id:
                    messagebox.showerror("Permission Denied", "You can only update your own clients.")
                    return

            broker_id_for_update = int(self.broker_id_var.get()) if self.broker_id_var.get() else None
            if self.role == "Broker":
                broker_id_for_update = self.user_id # Force broker_id to logged-in broker's ID

            updated_client = Client(
                id=client_id,
                name=self.name_var.get(),
                contact=self.contact_var.get(),
                preferences=self.preferences_var.get(),
                broker_id=broker_id_for_update
            )
            update_client(updated_client) 
            self.refresh_data()
            self.clear_form()
            messagebox.showinfo("Success", "Client updated successfully!")
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def delete_item(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a client to delete")
            return
        
        if messagebox.askyesno("Confirm", "Are you sure you want to delete this client?"):
            try:
                client_id = self.tree.item(selected[0])["values"][0]
                
                # If broker, ensure they can only delete their own clients
                if self.role == "Broker":
                    existing_client = get_client_by_id(client_id)
                    if existing_client and existing_client.broker_id != self.user_id:
                        messagebox.showerror("Permission Denied", "You can only delete your own clients.")
                        return

                delete_client(client_id)
                self.refresh_data()
                self.clear_form()
                messagebox.showinfo("Success", "Client deleted successfully!")
            except Exception as e:
                messagebox.showerror("Error", str(e))
    
    def clear_form(self):
        self.name_var.set("")
        self.contact_var.set("")
        self.preferences_var.set("")
        # For broker, pre-fill their ID and keep it read-only
        if self.role == "Broker":
            self.broker_id_var.set(str(self.user_id))
            self.broker_id_entry.config(state="readonly") 
        else:
            self.broker_id_var.set("")
            self.broker_id_entry.config(state="normal") # Enable for admin

    def _populate_form_fields(self, values):
        """Populates the Client form fields from selected treeview values."""
        # values: (id, name, contact, preferences, broker_id)
        if len(values) >= 5:
            self.name_var.set(values[1])
            self.contact_var.set(values[2])
            self.preferences_var.set(values[3])
            self.broker_id_var.set(values[4] if values[4] is not None else "") 
            # Ensure broker_id entry state is correct on populate
            if self.role == "Broker":
                self.broker_id_entry.config(state="readonly")
            else:
                self.broker_id_entry.config(state="normal")


class BrokerPanel(BasePanel):
    def __init__(self, parent, role, user_id):
        super().__init__(parent, role, user_id)
        self.setup_broker_ui()
    
    def setup_broker_ui(self):
        self.tree["columns"] = ("id", "name", "years_experience")
        self.tree.column("#0", width=0, stretch="no")
        self.tree.column("id", width=50)
        self.tree.column("name", width=150)
        self.tree.column("years_experience", width=150)
        
        self.tree.heading("id", text="ID")
        self.tree.heading("name", text="Name")
        self.tree.heading("years_experience", text="Years Experience")
        
        self.create_form_fields()
    
    def create_form_fields(self):
        ttk.Label(self.form_frame, text="Name:").grid(row=0, column=0, padx=5, pady=5)
        self.name_var = tk.StringVar()
        ttk.Entry(self.form_frame, textvariable=self.name_var).grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(self.form_frame, text="Years Experience:").grid(row=0, column=2, padx=5, pady=5)
        self.years_experience_var = tk.StringVar()
        ttk.Entry(self.form_frame, textvariable=self.years_experience_var).grid(row=0, column=3, padx=5, pady=5)
    
    def refresh_data(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Brokers panel always shows all brokers (only accessible by Admin)
        brokers = get_all_brokers() 
        for broker in brokers:
            self.tree.insert("", "end", values=(
                broker.id,
                broker.name,
                broker.years_experience
            ))
    
    def add_item(self):
        try:
            new_broker = Broker(
                id=None, 
                name=self.name_var.get(),
                years_experience=int(self.years_experience_var.get())
            )
            add_broker(new_broker) 
            self.refresh_data()
            self.clear_form()
            messagebox.showinfo("Success", "Broker added successfully!")
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def update_item(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a broker to update")
            return
        
        try:
            broker_id = self.tree.item(selected[0])["values"][0]
            updated_broker = Broker(
                id=broker_id,
                name=self.name_var.get(),
                years_experience=int(self.years_experience_var.get())
            )
            update_broker(updated_broker) 
            self.refresh_data()
            self.clear_form()
            messagebox.showinfo("Success", "Broker updated successfully!")
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def delete_item(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a broker to delete")
            return
        
        if messagebox.askyesno("Confirm", "Are you sure you want to delete this broker?"):
            try:
                broker_id = self.tree.item(selected[0])["values"][0]
                delete_broker(broker_id)
                self.refresh_data()
                self.clear_form()
                messagebox.showinfo("Success", "Broker deleted successfully!")
            except Exception as e:
                messagebox.showerror("Error", str(e))
    
    def clear_form(self):
        self.name_var.set("")
        self.years_experience_var.set("")

    def _populate_form_fields(self, values):
        """Populates the Broker form fields from selected treeview values."""
        # values: (id, name, years_experience)
        if len(values) >= 3:
            self.name_var.set(values[1])
            self.years_experience_var.set(values[2])

class PropertyPanel(BasePanel):
    def __init__(self, parent, role, user_id):
        super().__init__(parent, role, user_id)
        self.setup_property_ui()
    
    def setup_property_ui(self):
        self.tree["columns"] = ("id", "location", "type", "size", "price", "status")
        self.tree.column("#0", width=0, stretch="no")
        self.tree.column("id", width=50)
        self.tree.column("location", width=200)
        self.tree.column("type", width=100) 
        self.tree.column("size", width=100)
        self.tree.column("price", width=150)
        self.tree.column("status", width=100)
        
        self.tree.heading("id", text="ID")
        self.tree.heading("location", text="Location")
        self.tree.heading("type", text="Type") 
        self.tree.heading("size", text="Size (sqft)")
        self.tree.heading("price", text="Price")
        self.tree.heading("status", text="Status")
        
        self.create_form_fields()
    
    def create_form_fields(self):
        ttk.Label(self.form_frame, text="Location:").grid(row=0, column=0, padx=5, pady=5)
        self.location_var = tk.StringVar()
        ttk.Entry(self.form_frame, textvariable=self.location_var).grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(self.form_frame, text="Type:").grid(row=0, column=2, padx=5, pady=5)
        self.type_var = tk.StringVar()
        property_types = ['house', 'apartment', 'land', 'commercial'] 
        self.type_combobox = ttk.Combobox(self.form_frame, textvariable=self.type_var, values=property_types, state="readonly")
        self.type_combobox.grid(row=0, column=3, padx=5, pady=5)
        self.type_combobox.set('house') 

        ttk.Label(self.form_frame, text="Size:").grid(row=1, column=0, padx=5, pady=5)
        self.size_var = tk.StringVar()
        ttk.Entry(self.form_frame, textvariable=self.size_var).grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(self.form_frame, text="Price:").grid(row=1, column=2, padx=5, pady=5)
        self.price_var = tk.StringVar()
        ttk.Entry(self.form_frame, textvariable=self.price_var).grid(row=1, column=3, padx=5, pady=5)
        
        ttk.Label(self.form_frame, text="Status:").grid(row=2, column=0, padx=5, pady=5)
        self.status_var = tk.StringVar()
        statuses = ['available', 'sold'] 
        self.status_combobox = ttk.Combobox(self.form_frame, textvariable=self.status_var, values=statuses, state="readonly")
        self.status_combobox.grid(row=2, column=1, padx=5, pady=5)
        self.status_combobox.set('available') 
    
    def refresh_data(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # All roles can see all properties
        properties = get_all_properties() 
        for property_item in properties: 
            self.tree.insert("", "end", values=(
                property_item.id,
                property_item.location,
                property_item.type, 
                property_item.size,
                property_item.price,
                property_item.status
            ))
    
    def add_item(self):
        # Clients are disabled by BasePanel.create_buttons
        try:
            new_property = Property(
                id=None, 
                location=self.location_var.get(),
                type_=self.type_var.get(), 
                size=int(self.size_var.get()),
                price=float(self.price_var.get()), 
                status=self.status_var.get()
            )
            add_property(new_property) 
            self.refresh_data()
            self.clear_form()
            messagebox.showinfo("Success", "Property added successfully!")
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def update_item(self):
        # Clients are disabled by BasePanel.create_buttons
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a property to update")
            return
        
        try:
            property_id = self.tree.item(selected[0])["values"][0]
            updated_property = Property(
                id=property_id,
                location=self.location_var.get(),
                type_=self.type_var.get(), 
                size=int(self.size_var.get()),
                price=float(self.price_var.get()), 
                status=self.status_var.get()
            )
            update_property(updated_property) 
            self.refresh_data()
            self.clear_form()
            messagebox.showinfo("Success", "Property updated successfully!")
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def delete_item(self):
        # Clients are disabled by BasePanel.create_buttons
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a property to delete")
            return
        
        if messagebox.askyesno("Confirm", "Are you sure you want to delete this property?"):
            try:
                property_id = self.tree.item(selected[0])["values"][0]
                delete_property(property_id)
                self.refresh_data()
                self.clear_form()
                messagebox.showinfo("Success", "Property deleted successfully!")
            except Exception as e:
                messagebox.showerror("Error", str(e))
    
    def clear_form(self):
        self.location_var.set("")
        self.type_var.set("house") 
        self.size_var.set("")
        self.price_var.set("")
        self.status_var.set("available") 

    def _populate_form_fields(self, values):
        """Populates the Property form fields from selected treeview values."""
        # values: (id, location, type, size, price, status)
        if len(values) >= 6:
            self.location_var.set(values[1])
            self.type_var.set(values[2]) 
            self.size_var.set(values[3])
            
            try:
                price_val = float(values[4])
                self.price_var.set(f"{price_val:.1f}") 
            except ValueError:
                self.price_var.set(str(values[4])) 
            
            self.status_var.set(values[5]) 

class SalePanel(BasePanel):
    def __init__(self, parent, role, user_id):
        super().__init__(parent, role, user_id)
        self.setup_sale_ui()
        # For Broker role, ensure broker_id field is pre-filled and potentially read-only
        if self.role == "Broker":
            self.broker_id_var.set(str(self.user_id))
            # self.broker_id_entry.config(state="readonly") # Uncomment if you have an entry reference

    def setup_sale_ui(self):
        self.tree["columns"] = ("id", "property_id", "client_id", "broker_id", "date", "final_price")
        self.tree.column("#0", width=0, stretch="no")
        self.tree.column("id", width=50)
        self.tree.column("property_id", width=100)
        self.tree.column("client_id", width=100)
        self.tree.column("broker_id", width=100)
        self.tree.column("date", width=150)
        self.tree.column("final_price", width=150)
        
        self.tree.heading("id", text="ID")
        self.tree.heading("property_id", text="Property ID")
        self.tree.heading("client_id", text="Client ID")
        self.tree.heading("broker_id", text="Broker ID")
        self.tree.heading("date", text="Sale Date")
        self.tree.heading("final_price", text="Final Price")
        
        self.create_form_fields()
    
    def create_form_fields(self):
        ttk.Label(self.form_frame, text="Property ID:").grid(row=0, column=0, padx=5, pady=5)
        self.property_id_var = tk.StringVar()
        ttk.Entry(self.form_frame, textvariable=self.property_id_var).grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(self.form_frame, text="Client ID:").grid(row=0, column=2, padx=5, pady=5)
        self.client_id_var = tk.StringVar()
        ttk.Entry(self.form_frame, textvariable=self.client_id_var).grid(row=0, column=3, padx=5, pady=5)
        
        ttk.Label(self.form_frame, text="Broker ID:").grid(row=1, column=0, padx=5, pady=5)
        self.broker_id_var = tk.StringVar()
        # Store the entry widget reference to potentially disable it later
        self.broker_id_entry = ttk.Entry(self.form_frame, textvariable=self.broker_id_var)
        self.broker_id_entry.grid(row=1, column=1, padx=5, pady=5)

        # Disable broker_id entry for brokers
        if self.role == "Broker":
            self.broker_id_entry.config(state="readonly")
        
        ttk.Label(self.form_frame, text="Sale Date (YYYY-MM-DD):").grid(row=1, column=2, padx=5, pady=5)
        self.date_var = tk.StringVar()
        ttk.Entry(self.form_frame, textvariable=self.date_var).grid(row=1, column=3, padx=5, pady=5)
        
        ttk.Label(self.form_frame, text="Final Price:").grid(row=2, column=0, padx=5, pady=5)
        self.final_price_var = tk.StringVar()
        ttk.Entry(self.form_frame, textvariable=self.final_price_var).grid(row=2, column=1, padx=5, pady=5)
    
    def refresh_data(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        try:
            if self.role == "Broker":
                # Broker sees only their sales
                sales = get_sales_by_broker_id(self.user_id) # Use the broker's ID
            else:
                # Admin sees all sales (Client role won't see this tab)
                sales = get_all_sales() 
            
            for i, sale in enumerate(sales):
                formatted_date = sale.date.isoformat() if hasattr(sale.date, 'isoformat') else str(sale.date)
                formatted_price = f"{sale.final_price:.2f}" if isinstance(sale.final_price, (float, int, Decimal)) else str(sale.final_price)

                values_to_insert = (
                    str(sale.id),
                    str(sale.property_id),
                    str(sale.client_id),
                    str(sale.broker_id),
                    formatted_date, 
                    formatted_price
                )
                self.tree.insert("", "end", values=values_to_insert)
        except Exception as e:
            messagebox.showerror("Error", f"Error refreshing sales data: {e}")

    def add_item(self):
        try:
            property_id_val = int(self.property_id_var.get()) if self.property_id_var.get() else None
            client_id_val = int(self.client_id_var.get()) if self.client_id_var.get() else None
            broker_id_val = int(self.broker_id_var.get()) if self.broker_id_var.get() else None

            # For Broker role, auto-assign their ID
            if self.role == "Broker":
                broker_id_val = self.user_id 
            
            # --- Pre-check for existence of foreign keys ---
            if property_id_val is not None and not get_property_by_id(property_id_val):
                messagebox.showerror("Input Error", f"Property ID {property_id_val} does not exist.")
                return
            if client_id_val is not None and not get_client_by_id(client_id_val):
                messagebox.showerror("Input Error", f"Client ID {client_id_val} does not exist.")
                return
            if broker_id_val is not None and not get_broker_by_id(broker_id_val):
                messagebox.showerror("Input Error", f"Broker ID {broker_id_val} does not exist.")
                return
            # --- End pre-check ---

            sale_date_str = self.date_var.get()
            sale_date = datetime.date.fromisoformat(sale_date_str) if sale_date_str else None

            final_price_val = float(self.final_price_var.get()) if self.final_price_var.get() else None
            
            new_sale = Sale(
                id=None, 
                property_id=property_id_val,
                client_id=client_id_val,
                broker_id=broker_id_val,
                date=sale_date,
                final_price=final_price_val
            )
            add_sale(new_sale) 
            self.refresh_data()
            self.clear_form()
            messagebox.showinfo("Success", "Sale added successfully!")
        except ValueError:
            messagebox.showerror("Input Error", "Please ensure all ID and Price fields are valid numbers and Date is YYYY-MM-DD.")
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def update_item(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a sale to update")
            return
        
        try:
            sale_id = self.tree.item(selected[0])["values"][0]

            property_id_val = int(self.property_id_var.get()) if self.property_id_var.get() else None
            client_id_val = int(self.client_id_var.get()) if self.client_id_var.get() else None
            broker_id_val = int(self.broker_id_var.get()) if self.broker_id_var.get() else None

            # For Broker role, auto-assign their ID and check permission
            if self.role == "Broker":
                existing_sale = get_sale_by_id(sale_id)
                if existing_sale and existing_sale.broker_id != self.user_id:
                    messagebox.showerror("Permission Denied", "You can only update your own sales.")
                    return
                broker_id_val = self.user_id 

            # --- Pre-check for existence of foreign keys ---
            if property_id_val is not None and not get_property_by_id(property_id_val):
                messagebox.showerror("Input Error", f"Property ID {property_id_val} does not exist.")
                return
            if client_id_val is not None and not get_client_by_id(client_id_val):
                messagebox.showerror("Input Error", f"Client ID {client_id_val} does not exist.")
                return
            if broker_id_val is not None and not get_broker_by_id(broker_id_val):
                messagebox.showerror("Input Error", f"Broker ID {broker_id_val} does not exist.")
                return
            # --- End pre-check ---

            sale_date_str = self.date_var.get()
            sale_date = datetime.date.fromisoformat(sale_date_str) if sale_date_str else None

            final_price_val = float(self.final_price_var.get()) if self.final_price_var.get() else None

            updated_sale = Sale(
                id=sale_id,
                property_id=property_id_val,
                client_id=client_id_val,
                broker_id=broker_id_val,
                date=sale_date,
                final_price=final_price_val
            )
            update_sale(updated_sale) 
            self.refresh_data()
            self.clear_form()
            messagebox.showinfo("Success", "Sale updated successfully!")
        except ValueError:
            messagebox.showerror("Input Error", "Please ensure all ID and Price fields are valid numbers and Date is YYYY-MM-DD.")
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def delete_item(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a sale to delete")
            return
        
        if messagebox.askyesno("Confirm", "Are you sure you want to delete this sale?"):
            try:
                sale_id = self.tree.item(selected[0])["values"][0]
                
                # For Broker role, check permission
                if self.role == "Broker":
                    existing_sale = get_sale_by_id(sale_id)
                    if existing_sale and existing_sale.broker_id != self.user_id:
                        messagebox.showerror("Permission Denied", "You can only delete your own sales.")
                        return

                delete_sale(sale_id)
                self.refresh_data()
                self.clear_form()
                messagebox.showinfo("Success", "Sale deleted successfully!")
            except Exception as e:
                messagebox.showerror("Error", str(e))
    
    def clear_form(self):
        self.property_id_var.set("")
        self.client_id_var.set("")
        self.broker_id_var.set("")
        self.date_var.set("")
        self.final_price_var.set("")

    def _populate_form_fields(self, values):
        """Populates the Sale form fields from selected treeview values."""
        # values: (id, property_id, client_id, broker_id, date, final_price)
        if len(values) >= 6:
            self.property_id_var.set(values[1])
            self.client_id_var.set(values[2])
            self.broker_id_var.set(values[3])
            
            date_val = values[4]
            self.date_var.set(str(date_val)) 
            
            try:
                price_val = float(values[5])
                self.final_price_var.set(f"{price_val:.2f}") 
            except ValueError:
                self.final_price_var.set(str(values[5])) 
            
            # Ensure broker_id entry state is correct on populate
            if self.role == "Broker":
                self.broker_id_entry.config(state="readonly")
            else:
                self.broker_id_entry.config(state="normal")
