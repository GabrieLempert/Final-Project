from tkinter import filedialog
import tkinter as tk
from tkinter import messagebox


class CSVFileSelectorView:
    def __init__(self):
        """
        Constructor for the CSVFileSelectorView class. Initializes the GUI elements.
        """

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
        self.process_button = tk.Button(self.root, text="Process Entries")
        self.process_button.pack(pady=10)

        # Create a button to predict stock value
        self.predict_button = tk.Button(self.root, text="Predict")
        self.predict_button.pack(pady=10)

        # Create a separate window for selecting the machine learning model
        self.model_window = tk.Toplevel(self.root)
        self.model_window.withdraw()
        self.model_window_func()

    def model_window_func(self):
        """
        Helper method to initialize the GUI elements for the model selection window.
        """
        self.model1_button = tk.Button(self.model_window, text="Lasso")
        self.model2_button = tk.Button(self.model_window, text="DecisionTree Regressor")
        self.model3_button = tk.Button(self.model_window, text="Linear Regression")
        self.model4_button = tk.Button(self.model_window, text="Ridge")

    def on_button_click(self):
        """Callback function when 'Select CSV File' button is clicked"""
        file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if file_path:
            return file_path
        else:
            return None

    def show_warning(self, problem):
        """Show warning message box"""
        messagebox.showwarning(f'{problem}', "No file selected.")

    def process_entries(self):
        """Process entries from the entry boxes"""
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

    def show_model_menu(self):
        """Show model selection menu"""
        self.model_window.deiconify()
        self.model_window.title("Model Selector")
        self.model_window.geometry("200x200")
        for widget in self.model_window.winfo_children():
            if isinstance(widget, tk.Button):
                widget.pack(pady=10)

    def start(self):
        """Start the Tkinter event loop"""
        self.root.mainloop()

    def open_stock_prediction(self, predicted_stock_value, previous_stock_value):
        """Open a new window to display stock prediction information"""
        stock_prediction_window = tk.Toplevel()
        stock_prediction_window.title("Stock Prediction")

        # Create labels to display predicted stock value and previous stock value
        predicted_label = tk.Label(stock_prediction_window, text=f"Predicted Stock Value: {predicted_stock_value}")
        predicted_label.pack(pady=10)
        previous_label = tk.Label(stock_prediction_window, text=f"Previous Stock Value: {previous_stock_value}")
        previous_label.pack(pady=10)

        # Determine recommendation based on prediction and previous value
        recommendation = ""
        if predicted_stock_value > previous_stock_value:
            recommendation = "Invest Now"
        else:
            recommendation = "Sell Now"

        # Create label to display recommendation
        recommendation_label = tk.Label(stock_prediction_window, text=f"Recommendation: {recommendation}")
        recommendation_label.pack(pady=10)

        # Create a button to close the stock prediction window
        close_button = tk.Button(stock_prediction_window, text="Close", command=stock_prediction_window.destroy)
        close_button.pack(pady=10)

    def run(self):
        self.root.mainloop()
