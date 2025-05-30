import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from functools import partial

# Import all your panel classes directly from panels.py
from gui.panels import ClientPanel, BrokerPanel, PropertyPanel, SalePanel, BasePanel

# Import necessary controller for broker ID check
from controllers.broker_controller import get_broker_by_id

class RealEstateApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Real Estate System - Main Page")
        self.root.geometry("300x250")

        # Set a modern theme and custom styles
        style = ttk.Style()
        style.theme_use('clam')
        BasePanel.setup_styles() # Apply custom button styles

        self._setup_login_ui()

    def _setup_login_ui(self):
        """Sets up the initial login buttons on the main window."""
        label = ttk.Label(self.root, text="Login as:", font=("Arial", 16))
        label.pack(pady=20)

        btn_client = ttk.Button(
            self.root,
            text="Client",
            width=20,
            command=partial(self._create_dashboard_window, "Client", user_id=1), # Client ID hardcoded for demo
            style="Login.TButton"
        )
        btn_client.pack(pady=5)

        btn_broker = ttk.Button(
            self.root,
            text="Broker",
            width=20,
            command=self._show_broker_login_prompt,
            style="Login.TButton"
        )
        btn_broker.pack(pady=5)

        btn_admin = ttk.Button(
            self.root,
            text="Admin",
            width=20,
            command=partial(self._create_dashboard_window, "Admin", user_id=None), # Admin has no specific ID
            style="Login.TButton"
        )
        btn_admin.pack(pady=5)

    def _on_toplevel_closing(self, toplevel_window):
        """
        Handles closing of a Toplevel window.
        Destroys the Toplevel window and brings back the main root window.
        """
        toplevel_window.destroy()
        self.root.deiconify() # Show the main window again

    def _create_dashboard_window(self, role, user_id=None):
        """
        Creates and displays a new Toplevel window acting as a dashboard
        for the given role, hosting the appropriate panels in a Notebook.
        """
        self.root.withdraw() # Hide the main login window

        dashboard_window = tk.Toplevel(self.root)
        dashboard_window.title(f"{role} Dashboard")
        dashboard_window.geometry("1000x700")

        # Set protocol for closing the dashboard window
        dashboard_window.protocol("WM_DELETE_WINDOW", partial(self._on_toplevel_closing, dashboard_window))
        dashboard_window.grab_set() # Make dashboard modal

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

        # --- Role-based Tab Visibility ---
        if role == "Client":
            notebook.hide(client_tab)
            notebook.hide(broker_tab)
            notebook.hide(sale_tab)
            notebook.select(property_tab) # Default to properties tab
        elif role == "Broker":
            notebook.hide(broker_tab) # Brokers don't manage other brokers
            notebook.select(client_tab) # Default to clients tab for brokers
        elif role == "Admin":
            # Admin sees all tabs, no hiding needed
            notebook.select(client_tab) # Default to clients tab for admin

    def _show_broker_login_prompt(self):
        """Prompts the user for their Broker ID and validates it."""
        broker_id_input = simpledialog.askinteger(
            "Broker Login",
            "Enter your Broker ID:",
            parent=self.root # Attach to the main window
        )

        if broker_id_input is not None: # User didn't cancel the dialog
            broker = get_broker_by_id(broker_id_input)
            if broker:
                self._create_dashboard_window("Broker", user_id=broker_id_input)
            else:
                messagebox.showerror("Login Failed", f"Broker with ID {broker_id_input} does not exist. Please try again.")

    def run(self):
        """Starts the main Tkinter event loop."""
        self.root.mainloop()