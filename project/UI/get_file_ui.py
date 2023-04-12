import tkinter as tk
from tkinter import filedialog
import project.Predictor.predict_new as pn
csv_import = pn.CsvImport
def open_file_dialog(csv):
    file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
    if file_path:
        with open(file_path, "r") as file:
            lines = file.readlines()
    print(list(enumerate(lines)))




def process_entries():
    ticker = ticker_entry.get()
    owner_name = owner_name_entry.get()
    title = title_entry.get()
    transaction_type = transaction_type_entry.get()
    last_price = last_price_entry.get()
    quantity = quantity_entry.get()
    shares_held = shares_held_entry.get()
    owned = owned_entry.get()
    value = value_entry.get()
    stock_value = stock_value_entry.get()




# Create the main window
root = tk.Tk()
root.title("CSV File Selector")

# Create a button to open the file dialog
file_button = tk.Button(root, text="Select CSV File", command=lambda  :open_file_dialog(csv
                                                                                        =csv_import))
file_button.pack(pady=10)

# Create labels and entry boxes for additional options
ticker_label = tk.Label(root, text="Ticker:")
ticker_label.pack()
ticker_entry = tk.Entry(root)
ticker_entry.pack()

owner_name_label = tk.Label(root, text="Owner Name:")
owner_name_label.pack()
owner_name_entry = tk.Entry(root)
owner_name_entry.pack()

title_label = tk.Label(root, text="Title:")
title_label.pack()
title_entry = tk.Entry(root)
title_entry.pack()

transaction_type_label = tk.Label(root, text="Transaction Type:")
transaction_type_label.pack()
transaction_type_entry = tk.Entry(root)
transaction_type_entry.pack()

last_price_label = tk.Label(root, text="Last Price:")
last_price_label.pack()
last_price_entry = tk.Entry(root)
last_price_entry.pack()

quantity_label = tk.Label(root, text="Quantity:")
quantity_label.pack()
quantity_entry = tk.Entry(root)
quantity_entry.pack()

shares_held_label = tk.Label(root, text="Shares Held:")
shares_held_label.pack()
shares_held_entry = tk.Entry(root)
shares_held_entry.pack()

owned_label = tk.Label(root, text="Owned:")
owned_label.pack()
owned_entry = tk.Entry(root)
owned_entry.pack()

value_label = tk.Label(root, text="Value:")
value_label.pack()
value_entry = tk.Entry(root)
value_entry.pack()

stock_value_label = tk.Label(root, text="Stock Value:")
stock_value_label.pack()
stock_value_entry = tk.Entry(root)
stock_value_entry.pack()

# Create a button to process the entries
process_button = tk.Button(root, text="Process Entries", command=process_entries)
process_button.pack(pady=10)

# Start the Tkinter event loop
root.mainloop()
