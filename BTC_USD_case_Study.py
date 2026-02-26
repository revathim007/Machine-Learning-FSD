import yfinance as yf
import matplotlib.pyplot as plt

# Download last 6 months BTC-USD data
btc = yf.download("BTC-USD", period="6mo")

# Show first few rows
print(btc.head())

# Plot Closing Price
plt.figure(figsize=(10,5))
plt.plot(btc.index, btc['Close'])

plt.title("BTC-USD Closing Price - Last 6 Months")
plt.xlabel("Date")
plt.ylabel("Price (USD)")
plt.xticks(rotation=45)

plt.tight_layout()
plt.show()