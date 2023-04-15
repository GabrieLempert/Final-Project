import project.UI.get_file_ui as view
import project.Predictor.predict_new as model
class Controller:
    def __init__(self,view,model):
        self.view = view
        self.model = model
    def start_view(self):
        self.view.file_button.config(command=self.get_file)
        self.view.start()
    def get_file(self):
        file_path = self.view.on_button_click()
        if file_path:
            self.model.get_file(file_path)
            self.model.process_file()
            today = list(self.model.transactions.keys())[0]
            test = self.model.transactions[today]['Transaction 1']['data']
            print(test)
        else:
            self.view.show_message('No file path')









if __name__ == "__main__":
    model = model.Model()
    view = view.CSVFileSelectorView()
    controller  = Controller(view=view,model=model)
    controller.start_view()




