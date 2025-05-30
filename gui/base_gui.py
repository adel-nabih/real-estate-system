import tkinter as tk
from tkinter import ttk, messagebox
from controllers.broker_controller import get_all_brokers, add_broker, update_broker, delete_broker
from controllers.client_controller import get_all_clients, add_client, update_client, delete_client
from controllers.property_controller import get_all_properties, add_property, update_property, delete_property
from gui.panels import ClientPanel, BrokerPanel, PropertyPanel, SalePanel

class BaseGUI:
    def __init__(self, title):
        self.window = tk.Tk()
        self.window.title(title)
        self.window.geometry("1200x800")
        
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
    
    def on_closing(self):
        self.window.destroy()
    
    def run(self):
        self.window.mainloop() 