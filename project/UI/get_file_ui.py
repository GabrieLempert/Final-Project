from tkinter import filedialog
import tkinter as tk
from tkinter import messagebox

class CSVFileSelectorView:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("CSV File Selector")

        # Create a button to open the file dialog
        self.file_button = tk.Button(self.root, text="Select CSV File")
        self.file_button.pack(pady=10)

        # Create labels and entry boxes for additional options
        self.ticker_label = tk.Label(self.root, text="Ticker:")
        self.ticker_label.pack()
        self.ticker_entry = tk.Entry(self.root)
        self.ticker_entry.pack()

        self.owner_name_label = tk.Label(self.root, text="Owner Name:")
        self.owner_name_label.pack()
        self.owner_name_entry = tk.Entry(self.root)
        self.owner_name_entry.pack()

        self.title_label = tk.Label(self.root, text="Title:")
        self.title_label.pack()
        self.title_entry = tk.Entry(self.root)
        self.title_entry.pack()

        self.transaction_type_label = tk.Label(self.root, text="Transaction Type:")
        self.transaction_type_label.pack()
        self.transaction_type_entry = tk.Entry(self.root)
        self.transaction_type_entry.pack()

        self.last_price_label = tk.Label(self.root, text="Last Price:")
        self.last_price_label.pack()
        self.last_price_entry = tk.Entry(self.root)
        self.last_price_entry.pack()

        self.quantity_label = tk.Label(self.root, text="Quantity:")
        self.quantity_label.pack()
        self.quantity_entry = tk.Entry(self.root)
        self.quantity_entry.pack()

        self.shares_held_label = tk.Label(self.root, text="Shares Held:")
        self.shares_held_label.pack()
        self.shares_held_entry = tk.Entry(self.root)
        self.shares_held_entry.pack()

        self.owned_label = tk.Label(self.root, text="Owned:")
        self.owned_label.pack()
        self.owned_entry = tk.Entry(self.root)
        self.owned_entry.pack()

        self.value_label = tk.Label(self.root, text="Value:")
        self.value_label.pack()
        self.value_entry = tk.Entry(self.root)
        self.value_entry.pack()

        self.stock_value_label = tk.Label(self.root, text="Stock Value:")
        self.stock_value_label.pack()
        self.stock_value_entry = tk.Entry(self.root)
        self.stock_value_entry.pack()

        # Create a button to process the entries
        self.process_button = tk.Button(self.root, text="Process Entries",)
        self.process_button.pack(pady=10)

    def on_button_click(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if file_path:
            return file_path
        else:
            return None
    def show_message(self,problem):
        messagebox.showwarning(f'{problem}', "No file selected.")
    def process_entries(self):
        ticker = self.ticker_entry.get()
        owner_name = self.owner_name_entry.get()
        title = self.title_entry.get()
        transaction_type = self.transaction_type_entry.get()
        last_price = self.last_price_entry.get()
        quantity = self.quantity_entry.get()
        shares_held = self.shares_held_entry.get()
        owned = self.owned_entry.get()
        value = self.value_entry.get()
        stock_value = self.stock_value_entry.get()

    def start(self):
        # Start the Tkinter event loop
        self.root.mainloop()

# Usage:
