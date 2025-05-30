# gui/admin_gui.py

import tkinter as tk
from tkinter import ttk
from gui.base_gui import BaseGUI

class AdminGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Admin Dashboard")
        self.root.geometry("1200x800")
        
        # Create main container
        self.main_frame = ttk.Frame(root)
        self.main_frame.pack(expand=True, fill="both", padx=10, pady=10)
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.main_frame)
        self.notebook.pack(expand=True, fill="both")
        
        # Create panels
        from gui.panels import ClientPanel, BrokerPanel, PropertyPanel, SalePanel
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
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def on_closing(self):
        self.root.destroy()
