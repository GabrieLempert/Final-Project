import project.UI.get_file_ui as v
import project.Backend.predict_new as md
class Controller:
    def __init__(self, view_p, model_p):
        self.view = view_p
        self.model = model_p
        self.get_model_buttons()
    def start_view(self):
        self.view.file_button.config(command=self.get_file)
        self.view.start()
    def get_file(self):
        file_path = self.view.on_button_click()
        if file_path:
            self.model.get_file(file_path)
            self.model.process_file()
            self.model.create_imported_data()
            self.view.show_model_menu()
        else:
            self.view.show_warning('No file path')
    def get_model_buttons(self):
        self.view.model1_button.config(command=lambda :self.load_models_and_lose_window('Lasso'))
        self.view.model2_button.config(command=lambda :self.load_models_and_lose_window('DecisionTree Regressor'))
        self.view.model3_button.config(command=lambda :self.load_models_and_lose_window('Linear Regression'))
        self.view.model4_button.config(command=lambda :self.load_models_and_lose_window('Ridge'))
        self.view.predict_button.config(command=lambda :self.predict())
    def load_models_and_lose_window(self,text):
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
        today = self.model.today
        if self.model.transactions:
            last_key = max(self.model.transactions[today].keys(), key=md.key_function)
            transactions = self.model.transactions[today][last_key]
            if transactions['model'] is None:
                self.view.show_warning('No model yet')
            else:
                model_ml= transactions['model']
                data = transactions['data']
                stock_before = transactions['data'].stock_value
                result=self.model.predict_model(data=data,model=model_ml)[0]
                transactions[f'result for {model_ml.__class__.__name__}'] = result
                self.view.open_stock_prediction(predicted_stock_value=result,previous_stock_value=stock_before)
        else:
            self.view.show_warning('No File')





if __name__ == "__main__":
    model = md.Model()
    view = v.CSVFileSelectorView()
    controller  = Controller(view_p=view, model_p=model)
    controller.start_view()




