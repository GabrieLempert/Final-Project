# Final-Project


[Project Description]

This project serves as the culmination of our Bachelor's in Computer Science, representing the culmination of our extensive research and experimentation. Our main objective was to develop a sophisticated prediction model for stock prices, leveraging transaction data from shareholders as a valuable source of information.

## Data

The "data" folder in this repository contains the initial data obtained from Open Insider, spanning from 2021 to January 2023. This data was used for analysis and model training in our project.

### Data Source
- The data was obtained from Open Insider (https://www.openinsider.com), a website that provides insider trading data of publicly traded companies in the United States.

### Data Processing
- We used the data to analyze the transaction data of shareholders in order to predict stock prices.
- The data was processed and analyzed using Python programming language and various data manipulation libraries such as pandas and numpy.
- We used the Random Forest Regressor algorithm to train our predictive model, which gave the best results in our analysis.

### Data Cleaning
- The "stock_file.csv" file in the "data" folder was cleaned to eliminate tickers that do not exist or are not relevant to our project.
- We also created a new column called "in 30 days" in the cleaned dataset, which represents the target value for our stock price prediction.

### Create Data Script
- The "create_data.py" script, located in the "data" folder, is used to generate additional data for our analysis.
- Note that this script requires the "yahoo finance" library, which can be installed using the following command only:
- pip install -r project/Data/requirements.txt

# Installation

## Prerequisites
- Python 3.8.12 or higher installed
- Pip [version] installed

## Dependencies
The successful execution of this project requires the installation of the following Python packages, which can be easily accomplished using the provided `requirements.txt` file.

## bash
pip install -r requirements.txt

## The following packages with their corresponding versions are required:

tkinter 8.6
joblib 1.1.0
pandas 1.3.5
datetime 4.3
numpy 1.22.2
pickle 0.7.6
warnings 3.0.0
yfinacne 0.2.18

## Usage

1. Begin by cloning this repository to your local machine.
2. Navigate to the project directory.
3. Install the required dependencies by executing the pip install -r requirements.txt command.
4. Launch the Python script by running the python main.py command.

## Model-View-Controller (MVC) Architecture

This project follows the Model-View-Controller (MVC) architectural pattern for organizing and structuring the codebase. The model handles the data and business logic, the view is responsible for rendering the user interface, and the controller manages the interactions between the model and view components.
### Contributing

We highly value contributions to our project. If you are interested in contributing, please adhere to the following guidelines:

 Fork the repository and create a new branch to implement your changes.
Thoroughly test your changes to ensure their functionality.
 Submit a pull request with a descriptive title and detailed description of your modifications.
## License

### This project is licensed under the [Afeka Tel Aviv Academic College of Engineering](https://en.wikipedia.org/wiki/Afeka_College_of_Engineering) License.


### Acknowledgements

We extend our heartfelt appreciation to all those who have contributed to the development of this project, as well as the various resources and references that have guided our research and implementation.
