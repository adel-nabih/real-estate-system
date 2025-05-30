import tkinter as tk
from tkinter import ttk, messagebox # Import ttk for themed widgets and messagebox
from functools import partial 

# Import all your panel classes directly from panels.py
from gui.panels import ClientPanel, BrokerPanel, PropertyPanel, SalePanel, BasePanel 

# Global reference to the main root window
main_root_window = None

def on_toplevel_closing(toplevel_window):
    """
    Handles closing of a Toplevel window.
    Destroys the Toplevel window and brings back the main root window.
    """
    toplevel_window.destroy()
    if main_root_window:
        main_root_window.deiconify() # Show the main window again

def create_dashboard_window(role, user_id=None): # Added user_id parameter
    """
    Creates and displays a new Toplevel window acting as a dashboard
    for the given role, hosting the appropriate panels in a Notebook.
    """
    global main_root_window
    if main_root_window:
        main_root_window.withdraw() # Hide the main login window

    dashboard_window = tk.Toplevel(main_root_window)
    dashboard_window.title(f"{role} Dashboard")
    dashboard_window.geometry("1000x700") 

    dashboard_window.protocol("WM_DELETE_WINDOW", partial(on_toplevel_closing, dashboard_window))
    dashboard_window.grab_set() 

    notebook = ttk.Notebook(dashboard_window)
    notebook.pack(expand=True, fill="both", padx=10, pady=10)
    
    # Instantiate all panels, passing role and user_id
    client_tab = ClientPanel(notebook, role, user_id)
    broker_tab = BrokerPanel(notebook, role, user_id)
    property_tab = PropertyPanel(notebook, role, user_id)
    sale_tab = SalePanel(notebook, role, user_id)

    # Add all tabs first, then hide based on role
    notebook.add(client_tab, text="Clients")
    notebook.add(broker_tab, text="Brokers")
    notebook.add(property_tab, text="Properties")
    notebook.add(sale_tab, text="Sales")

    # --- Role-based Tab Visibility (from your preferred main.py) ---
    if role == "Client":
        # Use notebook.tab(widget, "text") for hiding by tab name, more robust
        notebook.hide(notebook.tab(client_tab, "text")) 
        notebook.hide(notebook.tab(broker_tab, "text")) 
        notebook.hide(notebook.tab(sale_tab, "text"))   
        notebook.select(property_tab) # Default to properties tab
    elif role == "Broker":
        notebook.hide(notebook.tab(broker_tab, "text")) # Brokers don't manage other brokers
        notebook.select(client_tab) # Default to clients tab for brokers
    elif role == "Admin":
        # Admin sees all tabs, no hiding needed
        notebook.select(client_tab) # Default to clients tab for admin

def main():
    global main_root_window 
    main_root_window = tk.Tk()
    main_root_window.title("Real Estate System - Main Page")
    main_root_window.geometry("300x250")

    # --- IMPORTANT: Set a modern theme FIRST, then apply custom styles ---
    style = ttk.Style()
    # Using 'clam' or 'alt' themes often provides better customizability
    style.theme_use('clam') 
    
    # Call setup_styles after theme is set (from panels.py)
    BasePanel.setup_styles() 

    # Changed tk.Label to ttk.Label to benefit from ttk styling
    label = ttk.Label(main_root_window, text="Login as:", font=("Arial", 16))
    label.pack(pady=20)

    # Changed tk.Button to ttk.Button for all login buttons and applied custom style
    # For testing, we'll use a placeholder user_id=1 for Client and Broker.
    # In a real app, this would come from your authentication system.
    btn_client = ttk.Button(main_root_window, text="Client", width=20, command=partial(create_dashboard_window, "Client", user_id=1), style="Login.TButton")
    btn_client.pack(pady=5)

    btn_broker = ttk.Button(main_root_window, text="Broker", width=20, command=partial(create_dashboard_window, "Broker", user_id=1), style="Login.TButton")
    btn_broker.pack(pady=5)

    btn_admin = ttk.Button(main_root_window, text="Admin", width=20, command=partial(create_dashboard_window, "Admin", user_id=None), style="Login.TButton") 
    btn_admin.pack(pady=5)

    main_root_window.mainloop()

if __name__ == "__main__":
    main()
