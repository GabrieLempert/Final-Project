import UI.get_file_ui as v
import Backend.predict_new as md

class Controller:
    def __init__(self, view_p, model_p):
        """
        Initializes the Controller with a view and a model.

        Args:
            view_p (v.CSVFileSelectorView): The view object for the UI.
            model_p (md.Model): The model object for the backend logic.
        """
        self.view = view_p
        self.model = model_p
        self.get_model_buttons()

    def start_view(self):
        """
        Starts the view by configuring the file button and showing the view.

        Returns:
            None
        """
        self.view.file_button.config(command=self.get_file)
        self.view.start()

    def get_file(self):
        """
        Gets the file path from the view, processes the file, and creates imported data.

        Returns:
            None
        """
        file_path = self.view.on_button_click()
        if file_path:
            self.model.get_file(file_path)
            self.model.process_file()
            self.model.create_imported_data()
            self.view.show_model_menu()
        else:
            self.view.show_warning('No file path')

    def get_model_buttons(self):
        """
        Configures the buttons in the view for selecting machine learning models.

        Returns:
            None
        """
        self.view.model1_button.config(command=lambda: self.load_models_and_lose_window('Lasso'))
        self.view.model2_button.config(command=lambda: self.load_models_and_lose_window('DecisionTree Regressor'))
        self.view.model3_button.config(command=lambda: self.load_models_and_lose_window('Linear Regression'))
        self.view.model4_button.config(command=lambda: self.load_models_and_lose_window('Ridge'))
        self.view.predict_button.config(command=lambda: self.predict())

    def load_models_and_lose_window(self, text):
        """
        Loads the selected machine learning model and hides the model selection window.

        Args:
            text (str): The text representing the selected machine learning model.

        Returns:
            None
        """
        if text == "Lasso":
            self.model.load_models('Lasso')
        elif text == "DecisionTree Regressor":
            self.model.load_models('DecisionTree Regressor')
        elif text == "Linear Regression":
            self.model.load_models('Linear Regression')
        elif text == "Ridge":
            self.model.load_models('Ridge')
        self.view.model_window.withdraw()

    def predict(self):
        """
        Predicts the target variable using the loaded machine learning model.

        Returns:
            None
        """
        today = self.model.today  # Get the current date from the model
        if self.model.transactions:  # Check if there are transactions in the model
            last_key = max(self.model.transactions[today].keys(),
                           key=md.key_function)  # Get the latest key from transactions for the current date using a custom key function
            transactions = self.model.transactions[today][last_key]  # Get the latest transaction for the current date
            if transactions['model'] is None:  # Check if the 'model' key in the transaction is None
                self.view.show_warning('No model yet')  # Show a warning in the view that no model has been loaded yet
            else:
                model_ml = transactions['model']  # Get the machine learning model from the transaction
                data = transactions['data']  # Get the data for prediction from the transaction
                stock_before = transactions['data'].stock_value  # Get the stock value before prediction from the data
                result = self.model.predict_model(data=data, model=model_ml)[
                    0]  # Predict the stock value using the loaded model and the data
                transactions[
                    f'result for {model_ml.__class__.__name__}'] = result  # Add the predicted result to the transaction with a key containing the name of the machine learning model
                self.view.open_stock_prediction(predicted_stock_value=result,
                                                previous_stock_value=stock_before)  # Open a stock prediction window in the view, showing the predicted stock value and the previous stock value
        else:
            self.view.show_warning('No File')  # Show a warning in the view that no file has been loaded yet


if __name__ == "__main__":
    model = md.Model()
    view = v.CSVFileSelectorView()
    controller = Controller(view_p=view, model_p=model)
    controller.start_view()
