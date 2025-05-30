import tkinter as tk
from tkinter import ttk
from .panels import ClientPanel, BrokerPanel, PropertyPanel, SalePanel

class Dashboard:
    def __init__(self, root, role):
        self.root = root
        self.role = role
        self.window = tk.Toplevel(root)
        self.window.title(f"Dashboard - {role.title()}")
        self.window.geometry("1200x800")
        self.center_window()
        
        # Create main container
        self.main_frame = ttk.Frame(self.window)
        self.main_frame.pack(expand=True, fill="both", padx=10, pady=10)
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.main_frame)
        self.notebook.pack(expand=True, fill="both")
        
        # Create panels
        self.client_panel = ClientPanel(self.notebook)
        self.broker_panel = BrokerPanel(self.notebook)
        self.property_panel = PropertyPanel(self.notebook)
        self.sale_panel = SalePanel(self.notebook)
        
        # Add panels to notebook
        self.notebook.add(self.client_panel, text="Clients")
        self.notebook.add(self.broker_panel, text="Brokers")
        self.notebook.add(self.property_panel, text="Properties")
        self.notebook.add(self.sale_panel, text="Sales")
        
        # Configure window close behavior
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def show(self):
        self.window.deiconify()
        self.window.grab_set()
    
    def on_closing(self):
        self.window.grab_release()
        self.window.destroy()
        self.root.deiconify()
    
    def center_window(self):
        self.window.update_idletasks()
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry(f"{width}x{height}+{x}+{y}") 