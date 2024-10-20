import pandas as pd
import matplotlib.pyplot as plt
import requests
import streamlit as st

# Set app and page title
st.set_page_config('Twelve Data Stock Price App')
st.title('Stock Price App (Using Twelve Data API)')

# Set sidebar settings (title and user input)
st.sidebar.header('User Input')
ticker_symbol = st.sidebar.text_input('Enter Stock Ticker (e.g., AAPL)', 'AAPL')

# Find a way to store API key more securely
API_KEY = '8369c61af12e444695d5df733ae144c2'

# Get stock data
def get_stock_data(ticker):
    url = f'https://api.twelvedata.com/time_series?symbol={ticker_symbol}&interval=1day&outputsize=100&apikey={API_KEY}'
    response = requests.get(url).json()
    # st.write(response)

    # Store data in DataFrame
    if 'values' in response:
        df = pd.DataFrame(response['values'])
        df['datetime'] = pd.to_datetime(df['datetime'])
        df.set_index('datetime', inplace = True)
        df = df.apply(pd.to_numeric, errors = 'coerce')
        return df
    else:
        return None

df = get_stock_data(ticker_symbol)

# If API works, display line chart of closing price
if df is not None:
    st.write(f'Daily stock price data for **{ticker_symbol}**')
    st.dataframe(df)

    st.write(f'Closing price for {ticker_symbol} over time')
    fig, ax = plt.subplots()
    ax.plot(df.index, df['close'], label = 'Close Price')
    ax.set_xlabel('Date')
    ax.set_ylabel('Price in USD')
    plt.title(f'{ticker_symbol} Stock Price')
    plt.xticks(rotation=45)
    st.pyplot(fig)

# If API doesn't work, display error message
else:
    st.error(f'Could not retrieve data for {ticker_symbol}. Please check the symbol or try again later.')
