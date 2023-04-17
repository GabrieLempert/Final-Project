import joblib
import pandas as pd
import datetime as dt
import numpy as np
import pickle
import warnings

"""""
In this section, a lambda function is defined as the key function for sorting. 
It takes an input 'x' and converts the last character of 'x' to an integer using the int() function.
The 'warnings' module is then used to filter out any warnings that may arise during the execution of this section, 
as specified by the 'filterwarnings('ignore')' statement.
"""""
warnings.filterwarnings('ignore')
key_function = lambda x: int(x[-1:])


class TitleFunctions:
    TITLES = ['vp', 'chief', 'chair', 'pres', 'chairman', 'cob']

    def __init__(self, title):
        """
        Constructor for TitleFunctions class.

        Parameters:
            title (str): Input title to be processed

        Description:
            Initializes the 'title' attribute by converting it to lowercase and removing 'co-' if present.
        """
        self.title = str.lower(title).replace('co-', '')

    def get_short_name(self, title):
        """
        Returns the shortened version of the input title.

        Parameters:
            title (str): Input title to be shortened

        Returns:
            (str): Shortened version of the input title, by taking the first character of each word in the title.
        """
        return ''.join([x[0] for x in title.split(' ')])

    def vp_function(self):
        """
        Performs processing for title 'vp'.

        Description:
            Calls the 'check_for_title' method with 'short_name' set to 'vp' and 'not_included' set to 'evp'.
        """
        self.check_for_title(short_name='vp', not_included='evp')

    def chief_function(self):
        """
        Performs processing for title 'chief'.

        Description:
            Calls the 'check_for_title' method without any additional parameters.
        """
        self.check_for_title()

    def chair_function(self):
        """
        Performs processing for title 'chair' or 'cob'.

        Description:
            Calls the 'check_for_title' method with 'short_name' set to 'cob'.
        """
        self.check_for_title(short_name='cob')

    def pres_function(self):
        """
        Performs processing for title 'pres'.

        Description:
            Calls the 'check_for_title' method with 'short_name' set to 'pres'.
        """
        self.check_for_title(short_name='pres')

    def apply_function_based_on_title(self, title):
        """
        Applies the appropriate processing based on the input title.

        Parameters:
            title (str): Input title to be processed

        Returns:
            (int): 0 if the input title is not in the list of allowed titles, otherwise None.
        """
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
            return 0

    def check_for_title(self, short_name=None, not_included=None):
        """
        Check and update the title of an object based on provided short_name and not_included parameters.

        Args:
            short_name (str, optional): The short name to set as the new title. Defaults to None.
            not_included (str, optional): The string that should not be included in the new title. Defaults to None.

        Returns:
            None

        Raises:
            None

        Example Usage:
            # Create an object with title "Chief Engineer"
            my_object = MyClass(title="Chief Engineer")

            # Call check_for_title with no parameters
            my_object.check_for_title()
            # The title will be updated to "Engineer"

            # Call check_for_title with short_name parameter
            my_object.check_for_title(short_name="Lead Engineer")
            # The title will be updated to "Lead Engineer"

            # Call check_for_title with not_included parameter
            my_object.check_for_title(not_included="Chief")
            # The title will be updated to "Lead Engineer"
        """
        if short_name is None and not_included is None:
            # If both short_name and not_included are not provided, update title based on default rules
            temp = self.get_short_name(self.title)
            if 'chief' in self.title:
                self.title = temp
        if short_name and not_included is None:
            # If short_name is provided but not_included is not provided, update title with short_name
            self.title = short_name
        if not_included and short_name:
            # If not_included and short_name are provided, update title with short_name if not_included is not present
            if short_name in self.title and not_included not in self.title:
                self.title = short_name


class InvalidValueException(Exception):
    def __init__(self, column_name, value):
        """
        Constructor for InvalidValueException class.

        Parameters:
            column_name (str): Name of the column where the invalid value was found.
            value (str): The invalid value that caused the exception.

        Description:
            Initializes the 'column_name', 'value', and 'message' attributes with appropriate values.
        """
        self.column_name = column_name
        self.value = value
        self.message = f"Invalid value '{value}' in column '{column_name}'."

    def __str__(self):
        """
        Returns the error message as a string.

        Returns:
            (str): The error message as a string.
        """
        return self.message


class ImportData:
    def __init__(self, transaction_date, trade_date, ticker, company_name, owner_name, title, transaction_type,
                 last_price, qty, shares_held, owned, value, stock_value):
        """
        Constructor for ImportData class.

        Parameters:
            transaction_date (str): Transaction date.
            trade_date (str): Trade date.
            ticker (str): Ticker symbol.
            company_name (str): Company name.
            owner_name (str): Owner name.
            title (str): Title.
            transaction_type (str): Transaction type.
            last_price (float): Last price.
            qty (int): Quantity.
            shares_held (int/str): Shares held.
            owned (int/str): Owned.
            value (int/str): Value.
            stock_value (float): Stock value.

        Description:
            Initializes the attributes of ImportData class with provided values.
        """
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
        """
        Sets the transaction type as 1 for 'P' or 'Purchase', and 0 for 'S' or 'Sale'.

        Parameters:
            transaction_type (str): Transaction type value.

        Returns:
            (int): 1 for 'P' or 'Purchase', 0 for 'S' or 'Sale'.

        Raises:
            InvalidValueException: If invalid transaction type is provided.
        """
        if 'P' or 'Purchase' in transaction_type:
            return 1
        elif 'S' or 'Sale' in transaction_type:
            return 0
        else:
            raise InvalidValueException('transaction_type', transaction_type)

    def set_owned(self, owned):
        """
        Sets the owned attribute as a decimal percentage from provided value.

        Parameters:
            owned (int/str): Owned value as either int or string.

        Returns:
            (float): Decimal percentage value of owned.
        """
        if type(owned) is str:
            return int(owned.replace('%', '')) / 100
        elif type(owned) is int:
            return owned / 100

    def set_shares_held(self, shares_held):
        """
        Sets the shares held attribute as an integer from provided value.

        Parameters:
            shares_held (int/str): Shares held value as either int or string.

        Returns:
            (int): Shares held value as integer.
        """
        if type(shares_held) is str:
            return shares_held.replace(',', '')
        elif type(shares_held) is int:
            return shares_held

    def set_value(self, value):
        """
        Sets the value attribute as an integer from provided value.

        Parameters:
            value (int/str): Value as either int or string.

        Returns:
            (int): Value as integer.
        """
        if type(value) is str:
            return value.replace(',', '').replace('$', '')
        elif type(value) is int:
            return value

    def change_attribute(self, attribute_name, dictionary, key):
        """
        Change the value of a specific attribute based on a provided key in a dictionary.

        Args:
            attribute_name (str): The name of the attribute to be changed.
            dictionary (dict): The dictionary containing the key-value pairs for attribute changes.
            key (str): The key to be used to retrieve the new value for the attribute.

        Raises:
            Exception: If the provided attribute_name does not exist.

        """
        if attribute_name == 'owner_name':
            # If key exists in dictionary, update owner_name attribute with the corresponding value
            if key in dictionary:
                self.owner_name = dictionary[key]
            else:
                # If key does not exist, add owner_name as a key in the dictionary with a value equal to the length
                # of the dictionary
                dictionary[self.owner_name] = len(dictionary)
        elif attribute_name == 'ticker':
            # If key exists in dictionary, update ticker attribute with the corresponding value
            if key in dictionary:
                self.ticker = dictionary[key]
            else:
                # If key does not exist, add owner_name as a key in the dictionary with a value equal to the length
                # of the dictionary
                dictionary[self.owner_name] = len(dictionary)
        else:
            # Raise an exception if the provided attribute_name does not exist
            raise Exception(f'{attribute_name} does not exist')

    def change_title(self, dictionary, key):
        """
        Change the value of the title attribute based on a provided key in a dictionary.

        Args:
            dictionary (dict): The dictionary containing the key-value pairs for title changes.
            key (str): The key to be used to retrieve the new value for the title.

        """
        title_before = TitleFunctions(key)
        for a_title in title_before.TITLES:
            if a_title in title_before.TITLES:
                title_before.apply_function_based_on_title(title=a_title)
        # Update the title attribute with the value retrieved from the dictionary using the title_before.title as the key
        self.title = dictionary[title_before.title]


class Model:
    """
    Class representing a model for transaction data analysis.
    The Model class provides methods for storing, analyzing, and predicting
    transaction data, as well as mapping job titles to ranks.
    """
    today = dt.date.today()  # Class level variable to store the current date

    def __init__(self):
        """
        Initializes a new instance of the Model class.
        """
        self.transactions = dict()  # Dictionary to store transaction data
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
        }  # Dictionary to store ranks for title mapping
        self.owner_names, self.ticker = pickle.load(open('Backend/encoded_dicts', 'rb'))
        # List to store owner names and ticker

    def get_file(self, file_path):
        """
        Reads a CSV file from the given file path and stores it as a transaction data frame.

        Args:
            file_path (str): The file path of the CSV file to read.

        Returns:
            int: The index of the transaction in the current date's transactions dictionary.
        """
        df = pd.read_csv(file_path)  # Read the CSV file
        if 1 == df.shape[0]:
            today = dt.date.today()  # Get the current date
            if today in self.transactions:  # If current date already exists in transactions
                last_key = len(self.transactions[today].keys()) + 1  # Get the index for the next transaction
                self.transactions[today][f'Transaction {last_key}'] = {'df': df}  # Store the transaction data frame
            else:  # If current date does not exist in transactions
                self.transactions[today] = {'Transaction 1': {'df': df}}  # Create a new entry for the first transaction
        return 0

    def process_file(self):
        """
        Processes the data in the latest transaction data frame for the current date.

        Retrieves the latest transaction data frame for the current date, applies a function to extract relevant data, and
        stores the extracted data as an instance of the ImportData class in the transaction's dictionary.
        """
        last_key = max(self.transactions[self.today].keys(), key=key_function)  # Get the key of the latest transaction
        df = self.transactions[self.today][last_key]['df']  # Get the data frame of the latest transaction
        result = df.apply(lambda x: x.iloc[0], axis=0)  # Apply a function to extract relevant data from the data frame
        data = ImportData(result[0], result[1], result[2], result[3], result[4], result[5], result[6], result[7],
                          result[8], result[9], result[10], result[11], result[12])  # Create an instance of ImportData
        self.transactions[self.today][last_key][
            'data'] = data  # Store the extracted data in the transactions dictionary

    def create_imported_data(self):
        """
        Creates a new instance of the ImportData class with updated owner name, ticker, and title.

        Retrieves the latest transaction key for the current date, and then retrieves the owner name, ticker, and title
        from the stored data of that transaction. Next, the corresponding attributes of the ImportData instance are updated
        with the current owner names, ticker, and ranks. Finally, the title of the ImportData instance is updated using the
        ranks attribute.
        """
        last_key = max(self.transactions[self.today].keys(), key=key_function)  # Get the key of the latest transaction
        owner_name = self.transactions[self.today][last_key][
            'data'].owner_name  # Get the owner name from the latest transaction
        ticker = self.transactions[self.today][last_key]['data'].ticker  # Get the ticker from the latest transaction
        title = self.transactions[self.today][last_key]['data'].title  # Get the title from the latest transaction

        # Update the attributes of the ImportData instance with the current owner names, ticker, and ranks
        self.transactions[self.today][last_key]['data'].change_attribute('owner_name', self.owner_names, owner_name)
        self.transactions[self.today][last_key]['data'].change_attribute('ticker', self.ticker, ticker)

        # Update the title of the ImportData instance using the ranks attribute
        self.transactions[self.today][last_key]['data'].change_title(self.ranks, title)

    def predict_model(self, data, model):
        """
        Predicts the target variable using the given data and machine learning model.

        Args:
            data (ImportData): The data instance containing the features for prediction.
            model (sklearn.base.BaseEstimator): The machine learning model for prediction.

        Returns:
            array-like: The predicted values of the target variable.
        """
        X = np.array([int(data.ticker), int(data.owner_name), int(data.title), int(data.transaction_type),
                      float(data.last_price), float(data.qty),
                      float(data.shares_held), float(data.owned), float(data.value), float(data.stock_value)]).reshape(
            1, -1)

        prediction = model.predict(X)
        return prediction

    def load_models(self, model):
        """
        Loads a machine learning model from a saved file and stores it in the transaction data.

        Args:
            model (str): The name of the machine learning model to be loaded.

        Returns:
            None
        """
        last_key = max(self.transactions[self.today].keys(), key=key_function)
        model_files = {
            'Lasso': 'Models/Lasso.joblib',
            'DecisionTree Regressor': 'Models/DecisionTreeRegressor.joblib',
            'Linear Regression': 'Models/LinearRegression.joblib',
            'Ridge': 'Models/Ridge.joblib'
        }

        model_ml = joblib.load(open(model_files[model], 'rb'))
        self.transactions[self.today][last_key]['model'] = model_ml
