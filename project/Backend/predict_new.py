import joblib
import pandas as pd
import datetime as dt
import numpy as np
import pickle
import warnings

warnings.filterwarnings('ignore')

key_function = lambda x: int(x[-1:])


class TitleFunctions:
    TITLES = ['vp', 'chief', 'chair', 'pres', 'chairman', 'cob']

    def __init__(self, title):
        self.title = str.lower(title).replace('co-', '')

    def get_short_name(self, title):
        return ''.join([x[0] for x in title.split(' ')])

    def vp_function(self):
        self.check_for_title(short_name='vp', not_included='evp')

    def chief_function(self):
        self.check_for_title()

    def chair_function(self):
        self.check_for_title(short_name='cob')

    def pres_function(self):
        self.check_for_title(short_name='pres')

    def apply_function_based_on_title(self, title):
        if title in self.TITLES:
            if title == 'vp':
                self.vp_function()
            elif title == 'chief':
                self.chief_function()
            elif title == 'chair':
                self.chair_function()
            elif title == 'pres':
                self.pres_function()
            elif title == 'chairman':
                self.chair_function()
            elif title == 'cob':
                self.chair_function()
        else:
            print("No function found for title:", title)

    def check_for_title(self, short_name=None, not_included=None):
        if short_name is None and not_included is None:
            temp = self.get_short_name(self.title)
            if 'chief' in self.title:
                self.title = temp
        if short_name and not_included is None:
            self.title = short_name
        if not_included and short_name:
            if short_name in self.title and not_included not in self.title:
                self.title = short_name


class InvalidValueException(Exception):
    """
    Custom exception to handle invalid values in a CSV column.
    """

    def __init__(self, column_name, value):
        self.column_name = column_name
        self.value = value
        self.message = f"Invalid value '{value}' in column '{column_name}'."

    def __str__(self):
        return self.message


class ImportData:
    def __init__(self, transaction_date, trade_date, ticker, company_name, owner_name, title, transaction_type,
                 last_price, qty, shares_held, owned, value, stock_value):
        self.transaction_date = transaction_date
        self.trade_date = trade_date
        self.ticker = ticker
        self.company_name = company_name
        self.owner_name = owner_name
        self.title = title
        self.transaction_type = self.set_transaction_type(transaction_type)
        self.last_price = last_price
        self.qty = qty
        self.shares_held = self.set_shares_held(shares_held)
        self.owned = self.set_owned(owned)
        self.value = self.set_value(value)
        self.stock_value = stock_value

    def set_transaction_type(self, transaction_type):
        if 'P' or 'Purchase' in transaction_type:
            return 1
        elif 'S' or 'Sale' in transaction_type:
            return 0
        else:
            raise InvalidValueException('transaction_type', transaction_type)

    def set_owned(self, owned):
        if type(owned) is str:
            return int(owned.replace('%', '')) / 100
        elif type(owned) is int:
            return owned / 100

    def set_shares_held(self, shares_held):
        if type(shares_held) is str:
            return shares_held.replace(',', '')
        elif type(shares_held) is int:
            return shares_held

    def set_value(self, value):
        if type(value) is str:
            return value.replace(',', '').replace('$', '')
        elif type(value) is int:
            return value

    def change_attribute(self, attribute_name, dictionary, key):
        if attribute_name == 'owner_name':
            if key in dictionary:
                self.owner_name = dictionary[key]
            else:
                dictionary[self.owner_name] = len(dictionary)
        elif attribute_name == 'ticker':
            if key in dictionary:
                self.ticker = dictionary[key]
            else:
                dictionary[self.owner_name] = len(dictionary)
        else:
            raise Exception(f'{attribute_name} does not exist')

    def change_title(self, dictionary, key):
        title_before = TitleFunctions(key)
        for a_title in title_before.TITLES:
            if a_title in title_before.TITLES:
                title_before.apply_function_based_on_title(title=a_title)
        self.title = dictionary[title_before.title]


class Model:
    today = dt.date.today()

    def __init__(self):
        self.transactions = dict()
        self.ranks = {
            'founder': 1,
            'cob': 2,
            'ceo': 2,
            'president': 3,
            'pres': 3,
            'evp': 3,
            'coo': 4,
            'cfo': 4,
            'cto': 4,
            'cio': 4,
            'chro': 4,
            'gc': 4,
            'vp': 5,
            'controller': 5,
            'cmo': 5,
            'cao': 5,
            'treasurer': 5,
            'secretary': 5,
            '10%': 5,
            'dir': 5
        }
        self.owner_names, self.ticker = pickle.load(open('Backend/encoded_dicts', 'rb'))

    def get_file(self, file_path):
        df = pd.read_csv(file_path)
        if 1 == df.shape[0]:
            today = dt.date.today()
            if today in self.transactions:
                last_key = len(self.transactions[today].keys()) + 1
                self.transactions[today][f'Transaction {last_key}'] = {'df': df}
                print(last_key)
            else:
                self.transactions[today] = {'Transaction 1': {'df': df}}
        return 0

    def process_file(self):
        last_key = max(self.transactions[self.today].keys(), key=key_function)
        df = self.transactions[self.today][last_key]['df']
        result = df.apply(lambda x: x.iloc[0], axis=0)
        data = ImportData(result[0], result[1], result[2], result[3], result[4], result[5], result[6], result[7],
                          result[8],
                          result[9], result[10], result[11], result[12])
        self.transactions[self.today][last_key]['data'] = data

    def create_imported_data(self):
        last_key = max(self.transactions[self.today].keys(), key=key_function)
        owner_name = self.transactions[self.today][last_key]['data'].owner_name
        ticker = self.transactions[self.today][last_key]['data'].ticker
        title = self.transactions[self.today][last_key]['data'].title
        self.transactions[self.today][last_key]['data'].change_attribute('owner_name', self.owner_names, owner_name)
        self.transactions[self.today][last_key]['data'].change_attribute('ticker', self.ticker, ticker)
        self.transactions[self.today][last_key]['data'].change_title(self.ranks, title)

    def predict_model(self, data, model):
        X = np.array([int(data.ticker), int(data.owner_name), int(data.title), int(data.transaction_type),float(data.last_price),float(data.qty),
                      float(data.shares_held),float(data.owned), float(data.value), float(data.stock_value)]).reshape(1, -1)

        prediction = model.predict(X)
        return prediction

    def load_models(self, model):
        last_key = max(self.transactions[self.today].keys(), key=key_function)
        model_files = {
            'Lasso': 'Models/Lasso.joblib',
            'DecisionTree Regressor': 'Models/DecisionTreeRegressor.joblib',
            'Linear Regression': 'Models/LinearRegression.joblib',
            'Ridge': 'Models/Ridge.joblib'
        }

        model_ml = joblib.load(open(model_files[model], 'rb'))
        self.transactions[self.today][last_key]['model'] = model_ml
