import streamlit as st
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Function to load historical data
def load_historical_data(symbol, start, end):
    data = yf.download(symbol, start=start, end=end)
    return data

# Function to load live market data
def load_live_data(symbol):
    data = yf.download(symbol, period="1d", interval="1m")
    return data

# Function to update the plot with new data
def update_plot(i, ax, symbol):
    live_stock_data = load_live_data(symbol)
    ax.clear()
    ax.plot(live_stock_data.index, live_stock_data['Close'], color='blue')
    ax.set_xlabel('Time')
    ax.set_ylabel('Price')
    ax.set_title('Live Market Data')

# Function to display historical data page
def historical_data_page():
    st.title('Historical Stock Price Data')

    stock_symbol = st.sidebar.text_input("Enter Stock Symbol", 'AAPL')
    start_date = st.sidebar.date_input("Start Date", pd.to_datetime('2023-01-01'))
    end_date = st.sidebar.date_input("End Date", pd.to_datetime('2024-01-01'))

    # Fetching historical data
    data_load_state = st.text('Loading data...')
    stock_data = load_historical_data(stock_symbol, start_date, end_date)
    data_load_state.text('Loading data...done!')

    # Display historical data
    if not stock_data.empty:
        st.subheader('Raw Data')
        st.write(stock_data.head())

        # Plotting closing price
        st.subheader('Closing Price')
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(stock_data.index, stock_data['Close'], color='blue')
        ax.set_xlabel('Date')
        ax.set_ylabel('Price')
        st.pyplot(fig)

        # Plotting volume
        st.subheader('Volume')
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.bar(stock_data.index, stock_data['Volume'], color='green')
        ax.set_xlabel('Date')
        ax.set_ylabel('Volume')
        st.pyplot(fig)
    else:
        st.error("No data available for the selected stock symbol and date range.")

# Function to display live market data page
def live_market_data_page():
    st.title('Live Market Data')

    live_stock_symbol = st.sidebar.text_input("Enter Stock Symbol", 'AAPL')

    # Create a Matplotlib figure and axis object
    fig, ax = plt.subplots(figsize=(10, 6))

    # Set up animation
    ani = animation.FuncAnimation(fig, update_plot, fargs=(ax, live_stock_symbol), interval=1000)

    # Display the Matplotlib figure using Streamlit's st.pyplot()
    st.pyplot(fig)

# Main function to run the app
def main():
    st.sidebar.title('User Input')
    page_selection = st.sidebar.radio("Select Page", ("Historical Data", "Live Market Data"))

    if page_selection == "Historical Data":
        historical_data_page()
    elif page_selection == "Live Market Data":
        live_market_data_page()

if __name__ == "__main__":
    main()
