# Stock Portfolio Tracker

A comprehensive stock portfolio tracking and analysis application designed to help users manage and analyze their stock investments.

## Features

- **Portfolio Management**: Track multiple portfolios and wallets
- **Performance Analysis**: Real-time performance tracking with statistical analysis
- **News Integration**: Latest financial news and market updates
- **Alerting System**: Customizable alerts for price movements and portfolio changes
- **Data Visualization**: Interactive charts and dashboards
- **Multi-User Support**: User account management and data isolation

## Technical Stack

- **UI Framework**: Streamlit for web interface
- **Data Analysis**: Pandas, NumPy for financial calculations
- **Market Data**: Yahoo Finance API integration
- **News**: Google News API for financial news
- **Deployment**: Azure cloud platform
- **AI Integration**: GPT for advanced analysis features

## Project Structure

```
stock_portfolio_tracker/
│
├── app/                    # Main application package
│   ├── api/                # API clients (finance, news)
│   ├── core/               # Business logic (portfolio management, alerts)
│   ├── data/               # Data models, database connections
│   ├── services/           # External service integrations (notifications, LLMs)
│   └── utils/              # Utility functions and helpers
│
├── ui/                     # Frontend components (Streamlit)
├── tests/                  # Unit and integration tests
├── sandboxes/              # Experimentation and prototyping space
├── scripts/                # Utility scripts (setup, DB migrations, etc.)
│
├── .gitignore              # Git exclusions
├── requirements.txt        # Production dependencies
├── requirements-dev.txt    # Development dependencies
├── README.md               # Project overview
└── .pre-commit-config.yaml # Pre-commit hooks configuration
```

## Setup

1. **Create virtual environment and install dependencies**:
   ```bash
   uv venv
   source .venv/bin/activate
   uv pip install -r requirements.txt
   ```

2. **Install development dependencies (optional)**:
   ```bash
   uv pip install -r requirements-dev.txt
   ```

3. **Set up environment variables**:
   ```bash
   cp .env.example .env
   # Edit .env with your API keys and configuration
   ```

4. **Run the application**:
   ```bash
   streamlit run ui/streamlit/main.py
   ```

## Development

- **Run tests**: `pytest`
- **Format code**: `black . && isort .`
- **Lint code**: `flake8`

## Contributing

## License

MIT License - see LICENSE file for details 