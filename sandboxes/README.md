# Portfolio Tracker Sandboxes

This directory contains sandbox environments for testing the four main components of the portfolio tracker system.

## 🏗️ Sandbox Overview

Each sandbox is designed to test specific functionality in isolation:

| Sandbox | Purpose | Key Features |
|---------|---------|--------------|
| **SQLite** | Database operations | Schema creation, queries, portfolio calculations |
| **Streamlit** | UI and visualization | Interactive dashboard, charts, user inputs |
| **Yahoo Finance** | Stock data retrieval | Real-time prices, historical data, financial metrics |
| **MCP Yahoo Finance** | MCP-based stock data | Real-time quotes, options chains, earnings calendar |
| **Google News** | News and sentiment | News aggregation, sentiment analysis, market news |

## 🚀 Quick Start

### Install Dependencies
```bash
# Install all dependencies from main requirements file
pip install -r requirements.txt
```

### Run Sandboxes

### 1. SQLite Sandbox
```bash
cd sandboxes/sqlite
python sqlite_sandbox.py
```
**Tests**: Database schema, sample data, portfolio queries

### 2. Streamlit Sandbox
```bash
cd sandboxes/streamlit
streamlit run streamlit_sandbox.py
```
**Tests**: UI components, interactive charts, data visualization

### 3. Yahoo Finance Sandbox
```bash
cd sandboxes/yfinance
python yfinance_sandbox.py
```
**Tests**: Stock data retrieval, financial metrics, portfolio analysis

### 4. MCP Yahoo Finance Sandbox
```bash
# Setup (first time only)
cd sandboxes/mcp_yahoo_finance
./setup.sh  # or python setup.py

# Run tests
python mcp_yahoo_finance_sandbox.py
```
**Tests**: MCP-based stock data, real-time quotes, options chains, earnings calendar

### 5. Google News Sandbox
```bash
cd sandboxes/news
python news_sandbox.py
```
**Tests**: News retrieval, sentiment analysis, market news

## 📋 What Each Sandbox Tests

### SQLite Sandbox
- ✅ Database connection and table creation
- ✅ Sample portfolio data insertion
- ✅ Complex SQL queries with JOINs
- ✅ Portfolio value calculations
- ✅ Gain/loss analysis

### Streamlit Sandbox
- ✅ Interactive web dashboard
- ✅ Real-time data visualization
- ✅ User input forms
- ✅ Responsive layout
- ✅ Chart interactions

### Yahoo Finance Sandbox
- ✅ Real-time stock data retrieval
- ✅ Historical price analysis
- ✅ Financial metrics calculation (Sharpe ratio, beta, etc.)
- ✅ Portfolio performance analysis
- ✅ Data visualization with matplotlib

### MCP Yahoo Finance Sandbox
- ✅ MCP-based stock data retrieval
- ✅ Real-time quotes and market data
- ✅ Options chain data
- ✅ Earnings calendar
- ✅ Stock search functionality
- ✅ Asynchronous data processing

### Google News Sandbox
- ✅ News article retrieval
- ✅ Stock-specific news searches
- ✅ Basic sentiment analysis
- ✅ News comparison across stocks
- ✅ Market news aggregation

## 🎯 Play Around Commands

### Test Individual Components
```bash
# Test database operations
cd sandboxes/sqlite && python sqlite_sandbox.py

# Test UI components
cd sandboxes/streamlit && streamlit run streamlit_sandbox.py

# Test stock data
cd sandboxes/yfinance && python yfinance_sandbox.py

# Test MCP stock data
cd sandboxes/mcp_yahoo_finance && python mcp_yahoo_finance_sandbox.py

# Test news retrieval
cd sandboxes/news && python news_sandbox.py
```

### Test Specific Features
```bash
# Test specific stock data
cd sandboxes/yfinance
python -c "from yfinance_sandbox import YahooFinanceSandbox; s=YahooFinanceSandbox(); print(s.get_stock_info('AAPL'))"

# Test news sentiment
cd sandboxes/news
python -c "from news_sandbox import GoogleNewsSandbox; s=GoogleNewsSandbox(); print(s.analyze_sentiment('Apple stock surges on strong earnings'))"
```

## 📊 Expected Outputs

### SQLite
- Database file: `portfolio_test.db`
- Console output with query results
- Portfolio calculations and metrics

### Streamlit
- Web dashboard at `http://localhost:8501`
- Interactive charts and tables
- Real-time data updates

### Yahoo Finance
- Stock comparison plots (PNG files)
- Financial metrics tables
- Portfolio analysis results

### MCP Yahoo Finance
- MCP stock comparison plots (PNG files)
- Real-time quote data
- Options chain data
- Earnings calendar data

### Google News
- JSON files with news data
- Sentiment analysis results
- News comparison tables

## 🔧 Troubleshooting

### Common Issues
1. **Dependencies**: Make sure to install requirements for each sandbox
2. **Rate Limits**: Yahoo Finance, MCP Yahoo Finance, and Google News have rate limits
3. **Network**: Some sandboxes require internet connection
4. **Ports**: Streamlit uses port 8501 by default
5. **Node.js**: MCP Yahoo Finance requires Node.js and npm

### Environment Setup
```bash
# Install all dependencies from main requirements file
pip install -r requirements.txt
```

## 🎨 Customization Ideas

### SQLite
- Add more tables (transactions, dividends, etc.)
- Create new query types
- Add data validation

### Streamlit
- Add new chart types
- Create multi-page apps
- Add user authentication

### Yahoo Finance
- Add more technical indicators
- Create backtesting scenarios
- Add international stocks

### MCP Yahoo Finance
- Add more MCP server integrations
- Implement caching and connection pooling
- Add synchronous wrapper for easier integration

### Google News
- Improve sentiment analysis
- Add news categorization
- Create news alerts

## 📝 Notes

- All sandboxes use sample data for testing
- Some features require internet connection
- Rate limits apply to external APIs
- Sandboxes are designed for development/testing only
- Production code should include proper error handling and security measures 