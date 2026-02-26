# get data for BTC-USD using yfinance
import yfinance as yf
import pandas as pd
import numpy  as np

def get_btc_data():
    

    print("--- Fetching Bitcoin (BTC-USD) Data ---")

    ticker_symbol = "BTC-USD"
    btc = yf.Ticker(ticker_symbol)

    
    hist = btc.history(period="180d")

    print(hist[['Open', 'High', 'Low', 'Close', 'Volume']])

    
    hist['MA9'] = hist['Close'].rolling(window=9).mean()
    hist['MA21'] = hist['Close'].rolling(window=21).mean()

    
    hist['uptrend'] = np.where(hist['Close'] > hist['MA21'], 1, 0)
    hist['upcross'] = np.where(
        (hist['uptrend'] == 1) & (hist['uptrend'].shift(1) == 0),
        hist['Close'],
        0
    )

    hist['downtrend'] = np.where(hist['Close'] < hist['MA21'], 1, 0)
    hist['downcross'] = np.where(
        (hist['downtrend'] == 1) & (hist['downtrend'].shift(1) == 0),
        hist['Close'],
        0
    )

    total = 0
    start_price = 0

    for i in range(1, len(hist)):

        if hist['upcross'].iloc[i] != 0:
            start_price = hist['upcross'].iloc[i]
            print(f"Buy on {hist.index[i]} at {start_price}")

        if hist['downcross'].iloc[i] != 0 and start_price != 0:
            end_price = hist['downcross'].iloc[i]
            print(f"Sell on {hist.index[i]} at {end_price}")

            profit = end_price - start_price
            total += profit

            print(f"Profit: {profit}")
            print(f"Profit %: {(profit / start_price) * 100:.2f}%")
            start_price = 0

    print(f"\nTotal Profit: {total}")

    
    hist.to_csv("btc_usd.csv")

    
    import plotly.graph_objects as go

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=hist.index,
        y=hist['Close'],
        mode='lines',
        name='Close Price'
    ))

    fig.add_trace(go.Scatter(
        x=hist.index,
        y=hist['MA9'],
        mode='lines',
        name='MA9'
    ))

    fig.add_trace(go.Scatter(
        x=hist.index,
        y=hist['MA21'],
        mode='lines',
        name='MA21'
    ))

    fig.update_layout(
        title='BTC-USD Close Price and Moving Averages',
        xaxis_title='Date',
        yaxis_title='Price (USD)'
    )

    fig.show()


if __name__ == "__main__":
    get_btc_data()