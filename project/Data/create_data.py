import yfinance as yf
import pandas as pd
import threading

df = pd.read_csv('stock_file.csv')

# Define a lock for thread synchronization
lock = threading.Lock()


# Convert the tickers column to a list
tickers = df['ticker'].unique().tolist()

def get_stock_value_30_days_later(date, ticker):
    try:
        if ticker == 'FB':
            ticker = 'META'
        stock = yf.Ticker(ticker)
        history = stock.history(start=date, end=pd.to_datetime(date) + pd.DateOffset(days=30))
        if history['Close'].to_list().__len__() != 0:
            print(f'{ticker} has History and date is {date}')
            return history['Close']
        else:
            return [0, 0]
    except:
        return [0,0]

# Define a function that will be run by each thread
def process_rows(start_index, end_index):
    for index in range(start_index, end_index):
        symbol = df.at[index, 'ticker']
        date = df.at[index, 'trade_date']
        stocks = [get_stock_value_30_days_later(date, symbol)[0], get_stock_value_30_days_later(date, symbol)[-1]]
        # Acquire the lock before updating the dataframe
        lock.acquire()
        df.at[index, 'stock_value'] = stocks[0]
        df.at[index, '30_days_later'] = stocks[1]
        lock.release()

# Split the dataframe into 4 equal parts
chunk_size = len(df) // 4
chunks = [(i * chunk_size, (i + 1) * chunk_size) for i in range(4)]
chunks[-1] = (chunks[-1][0], len(df))

# Create a list to hold the threads
threads = []

# Start each thread, passing in the start and end indices of its assigned chunk
for start, end in chunks:
    t = threading.Thread(target=process_rows, args=(start, end))
    threads.append(t)
    t.start()

# Wait for all threads to finish before continuing
for t in threads:
    t.join()

# Save the updated dataframe to a new file
df.to_csv('final_stock_file.csv', index=False)


