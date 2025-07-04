# Yahoo Finance Sandbox

Test stock data retrieval and analysis using Yahoo Finance API.

## What to Test

- Stock information retrieval
- Historical price data
- Financial metrics calculation
- Portfolio analysis
- Data visualization
- Multiple stock comparison

## Commands to Run

```bash
# Navigate to sandbox directory
cd sandboxes/yfinance

# Install dependencies (from main repo)
pip install -r ../../requirements.txt

# Run the Yahoo Finance sandbox
python yfinance_sandbox.py

# Test specific features
python -c "
from yfinance_sandbox import YahooFinanceSandbox
sandbox = YahooFinanceSandbox()
info = sandbox.get_stock_info('AAPL')
print(info)
"
```

## Expected Output

You should see:
- ✅ Stock information for AAPL, GOOGL, MSFT
- ✅ Historical data retrieval
- 📊 Financial metrics comparison table
- 💼 Portfolio analysis results
- 📈 Stock comparison plot (saved as PNG)

## Features to Test

1. **Stock Info**: Get company details, prices, ratios
2. **Historical Data**: Retrieve price history with calculated metrics
3. **Financial Metrics**: Calculate returns, volatility, Sharpe ratio, beta
4. **Portfolio Analysis**: Analyze weighted portfolios
5. **Data Visualization**: Create comparison charts
6. **Multiple Stocks**: Compare several stocks at once

## Sample Data Generated

- Stock comparison plots (PNG files)
- Financial metrics tables
- Portfolio analysis results
- Historical price data

## Play Around Ideas

1. Test different stock symbols
2. Modify time periods (1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max)
3. Add new financial metrics
4. Create different portfolio weightings
5. Test with international stocks
6. Add technical indicators (RSI, MACD, etc.)
7. Create backtesting scenarios
8. Test with ETFs and mutual funds

## Troubleshooting

- **Rate Limits**: Yahoo Finance may limit requests, use delays between calls
- **No Data**: Some symbols might not have data, try popular stocks
- **Network Issues**: Check internet connection
- **Plot Display**: Make sure matplotlib backend is configured for your environment

## API Limitations

- Yahoo Finance is free but has rate limits
- Some data might be delayed
- Not all stocks have complete information
- International stocks may have limited data 