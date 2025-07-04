#!/usr/bin/env python3
"""
Yahoo Finance Sandbox for Portfolio Tracker
Test stock data retrieval and analysis using yfinance
"""

import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Dict, List, Optional, Tuple
import warnings

warnings.filterwarnings("ignore")


class YahooFinanceSandbox:
    def __init__(self):
        self.tickers = []
        self.data = {}

    def get_stock_info(self, symbol: str) -> Dict:
        """Get basic stock information"""
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info

            # Extract key information
            stock_info = {
                "Symbol": symbol,
                "Name": info.get("longName", "N/A"),
                "Sector": info.get("sector", "N/A"),
                "Industry": info.get("industry", "N/A"),
                "Market Cap": info.get("marketCap", 0),
                "Current Price": info.get("currentPrice", 0),
                "52 Week High": info.get("fiftyTwoWeekHigh", 0),
                "52 Week Low": info.get("fiftyTwoWeekLow", 0),
                "P/E Ratio": info.get("trailingPE", 0),
                "Dividend Yield": info.get("dividendYield", 0),
                "Volume": info.get("volume", 0),
                "Beta": info.get("beta", 0),
            }

            print(f"✅ Retrieved info for {symbol}")
            return stock_info

        except Exception as e:
            print(f"❌ Error getting info for {symbol}: {e}")
            return {}

    def get_historical_data(
        self, symbol: str, period: str = "1y"
    ) -> pd.DataFrame:
        """Get historical price data"""
        try:
            ticker = yf.Ticker(symbol)
            hist = ticker.history(period=period)

            if hist.empty:
                print(f"⚠️  No data found for {symbol}")
                return pd.DataFrame()

            # Convert timezone-aware index to timezone-naive
            if hist.index.tz is not None:
                hist.index = hist.index.tz_localize(None)

            # Calculate additional metrics
            hist["Daily_Return"] = hist["Close"].pct_change()
            hist["Cumulative_Return"] = (1 + hist["Daily_Return"]).cumprod()
            hist["Volatility"] = hist["Daily_Return"].rolling(window=20).std()

            print(f"✅ Retrieved {len(hist)} days of data for {symbol}")
            return hist

        except Exception as e:
            print(f"❌ Error getting historical data for {symbol}: {e}")
            return pd.DataFrame()

    def get_multiple_stocks(
        self, symbols: List[str], period: str = "1y"
    ) -> Dict[str, pd.DataFrame]:
        """Get data for multiple stocks"""
        data = {}
        for symbol in symbols:
            data[symbol] = self.get_historical_data(symbol, period)
        return data

    def calculate_metrics(self, symbol: str, data: pd.DataFrame) -> Dict:
        """Calculate key financial metrics"""
        if data.empty:
            return {}

        # Basic metrics
        current_price = data["Close"].iloc[-1]
        start_price = data["Close"].iloc[0]
        total_return = (current_price - start_price) / start_price * 100

        # Volatility (annualized)
        daily_returns = data["Daily_Return"].dropna()
        volatility = daily_returns.std() * np.sqrt(252) * 100

        # Sharpe ratio (assuming risk-free rate of 2%)
        risk_free_rate = 0.02
        excess_returns = daily_returns - risk_free_rate / 252
        sharpe_ratio = (
            excess_returns.mean() / daily_returns.std() * np.sqrt(252)
        )

        # Maximum drawdown
        cumulative_returns = (1 + daily_returns).cumprod()
        running_max = cumulative_returns.expanding().max()
        drawdown = (cumulative_returns - running_max) / running_max
        max_drawdown = drawdown.min() * 100

        # Beta (if we have market data)
        # For simplicity, using S&P 500 as market proxy
        try:
            market_data = yf.Ticker("^GSPC").history(period="1y")
            market_returns = market_data["Close"].pct_change().dropna()

            # Align dates
            common_dates = daily_returns.index.intersection(
                market_returns.index
            )
            if len(common_dates) > 30:
                stock_returns_aligned = daily_returns.loc[common_dates]
                market_returns_aligned = market_returns.loc[common_dates]

                # Calculate beta
                covariance = np.cov(
                    stock_returns_aligned, market_returns_aligned
                )[0, 1]
                market_variance = np.var(market_returns_aligned)
                beta = (
                    covariance / market_variance if market_variance != 0 else 0
                )
            else:
                beta = 0
        except:
            beta = 0

        metrics = {
            "Symbol": symbol,
            "Current Price": round(current_price, 2),
            "Total Return (%)": round(total_return, 2),
            "Volatility (%)": round(volatility, 2),
            "Sharpe Ratio": round(sharpe_ratio, 3),
            "Max Drawdown (%)": round(max_drawdown, 2),
            "Beta": round(beta, 3),
            "Days of Data": len(data),
        }

        return metrics

    def compare_stocks(
        self, symbols: List[str], period: str = "1y"
    ) -> pd.DataFrame:
        """Compare multiple stocks"""
        print(f"\n📊 Comparing {len(symbols)} stocks over {period} period...")

        all_metrics = []
        all_data = self.get_multiple_stocks(symbols, period)

        for symbol, data in all_data.items():
            if not data.empty:
                metrics = self.calculate_metrics(symbol, data)
                all_metrics.append(metrics)

        if all_metrics:
            comparison_df = pd.DataFrame(all_metrics)
            return comparison_df
        else:
            return pd.DataFrame()

    def create_portfolio_analysis(
        self, portfolio: Dict[str, float], period: str = "1y"
    ) -> Dict:
        """Analyze a portfolio of stocks with weights"""
        print(f"\n💼 Portfolio Analysis for {len(portfolio)} stocks...")

        symbols = list(portfolio.keys())
        weights = list(portfolio.values())

        # Get data for all stocks
        all_data = self.get_multiple_stocks(symbols, period)

        # Find common date range for all stocks
        all_dates = []
        for symbol, data in all_data.items():
            if not data.empty:
                all_dates.extend(data.index.tolist())

        if not all_dates:
            print("❌ No data available for portfolio analysis")
            return {}

        # Get unique dates and sort them
        common_dates = sorted(set(all_dates))

        # Calculate portfolio returns using actual data dates
        portfolio_returns = pd.Series(0.0, index=common_dates)

        for symbol, weight in zip(symbols, weights):
            if symbol in all_data and not all_data[symbol].empty:
                returns = all_data[symbol]["Daily_Return"].fillna(0)
                # Align returns with common dates
                aligned_returns = returns.reindex(common_dates, fill_value=0)
                portfolio_returns += aligned_returns * weight

        # Portfolio metrics
        total_return = (1 + portfolio_returns).prod() - 1
        volatility = portfolio_returns.std() * np.sqrt(252)
        sharpe_ratio = (
            (portfolio_returns.mean() * 252 - 0.02) / volatility
            if volatility > 0
            else 0
        )

        # Individual stock metrics
        stock_metrics = []
        for symbol, weight in zip(symbols, weights):
            if symbol in all_data and not all_data[symbol].empty:
                metrics = self.calculate_metrics(symbol, all_data[symbol])
                metrics["Weight"] = weight
                stock_metrics.append(metrics)

        portfolio_analysis = {
            "Portfolio Total Return (%)": round(total_return * 100, 2),
            "Portfolio Volatility (%)": round(volatility * 100, 2),
            "Portfolio Sharpe Ratio": round(sharpe_ratio, 3),
            "Number of Stocks": len(portfolio),
            "Stock Metrics": pd.DataFrame(stock_metrics)
            if stock_metrics
            else pd.DataFrame(),
        }

        return portfolio_analysis

    def plot_stock_comparison(self, symbols: List[str], period: str = "1y"):
        """Create comparison plots for multiple stocks"""
        print(f"\n📈 Creating comparison plots for {len(symbols)} stocks...")

        all_data = self.get_multiple_stocks(symbols, period)

        if not all_data:
            print("❌ No data available for plotting")
            return

        # Normalize prices to start at 100 for comparison
        normalized_data = {}
        for symbol, data in all_data.items():
            if not data.empty:
                normalized_data[symbol] = (
                    data["Close"] / data["Close"].iloc[0]
                ) * 100

        # Create comparison plot
        plt.figure(figsize=(12, 8))

        for symbol, normalized_prices in normalized_data.items():
            plt.plot(
                normalized_prices.index,
                normalized_prices.values,
                label=symbol,
                linewidth=2,
            )

        plt.title(f"Stock Price Comparison (Normalized to 100)", fontsize=16)
        plt.xlabel("Date", fontsize=12)
        plt.ylabel("Normalized Price", fontsize=12)
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.tight_layout()

        # Save plot
        plot_filename = (
            f"stock_comparison_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        )
        plt.savefig(plot_filename, dpi=300, bbox_inches="tight")
        print(f"✅ Saved comparison plot as {plot_filename}")
        plt.show()

    def test_all_features(self):
        """Test all sandbox features"""
        print("🚀 Yahoo Finance Sandbox - Testing All Features")
        print("=" * 60)

        # Test stocks
        test_symbols = ["AAPL", "GOOGL", "MSFT", "TSLA", "AMZN"]

        # 1. Get stock information
        print("\n1. 📋 Getting Stock Information:")
        for symbol in test_symbols[:3]:  # Test first 3 to avoid rate limits
            info = self.get_stock_info(symbol)
            if info:
                print(
                    f"   {symbol}: {info['Name']} - ${info['Current Price']:.2f}"
                )

        # 2. Get historical data
        print("\n2. 📊 Getting Historical Data:")
        for symbol in test_symbols[:3]:
            data = self.get_historical_data(symbol, "6mo")
            if not data.empty:
                print(f"   {symbol}: {len(data)} days of data")

        # 3. Calculate metrics
        print("\n3. 📈 Calculating Metrics:")
        comparison = self.compare_stocks(test_symbols[:3], "6mo")
        if not comparison.empty:
            print(
                comparison[
                    [
                        "Symbol",
                        "Total Return (%)",
                        "Volatility (%)",
                        "Sharpe Ratio",
                    ]
                ].to_string(index=False)
            )

        # 4. Portfolio analysis
        print("\n4. 💼 Portfolio Analysis:")
        portfolio = {"AAPL": 0.4, "GOOGL": 0.3, "MSFT": 0.3}
        portfolio_analysis = self.create_portfolio_analysis(portfolio, "6mo")

        if portfolio_analysis:
            print(
                f"   Portfolio Return: {portfolio_analysis['Portfolio Total Return (%)']}%"
            )
            print(
                f"   Portfolio Volatility: {portfolio_analysis['Portfolio Volatility (%)']}%"
            )
            print(
                f"   Portfolio Sharpe Ratio: {portfolio_analysis['Portfolio Sharpe Ratio']}"
            )

        # 5. Create plots
        print("\n5. 📊 Creating Plots:")
        self.plot_stock_comparison(test_symbols[:3], "6mo")

        print("\n✅ All Yahoo Finance tests completed!")


def main():
    """Main function to run Yahoo Finance sandbox tests"""
    sandbox = YahooFinanceSandbox()
    sandbox.test_all_features()


if __name__ == "__main__":
    main()
