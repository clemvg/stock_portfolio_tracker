#!/usr/bin/env python3
"""
Streamlit Sandbox for Portfolio Tracker
Test UI components and data visualization
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import random

# Page configuration
st.set_page_config(
    page_title="Portfolio Tracker Sandbox",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)


def create_sample_data():
    """Create sample portfolio data"""
    stocks = [
        {"symbol": "AAPL", "name": "Apple Inc.", "sector": "Technology"},
        {"symbol": "GOOGL", "name": "Alphabet Inc.", "sector": "Technology"},
        {
            "symbol": "MSFT",
            "name": "Microsoft Corporation",
            "sector": "Technology",
        },
        {"symbol": "TSLA", "name": "Tesla Inc.", "sector": "Automotive"},
        {
            "symbol": "AMZN",
            "name": "Amazon.com Inc.",
            "sector": "Consumer Discretionary",
        },
    ]

    portfolio_data = []
    for stock in stocks:
        shares = random.randint(5, 50)
        purchase_price = random.uniform(100, 3000)
        current_price = purchase_price * random.uniform(0.8, 1.3)

        portfolio_data.append(
            {
                "Symbol": stock["symbol"],
                "Company": stock["name"],
                "Sector": stock["sector"],
                "Shares": shares,
                "Purchase Price": round(purchase_price, 2),
                "Current Price": round(current_price, 2),
                "Total Invested": round(shares * purchase_price, 2),
                "Current Value": round(shares * current_price, 2),
                "Gain/Loss": round(
                    (shares * current_price) - (shares * purchase_price), 2
                ),
                "Gain/Loss %": round(
                    ((current_price - purchase_price) / purchase_price) * 100, 2
                ),
            }
        )

    return pd.DataFrame(portfolio_data)


def create_price_history():
    """Create sample price history data"""
    dates = pd.date_range(start="2024-01-01", end="2024-03-01", freq="D")
    symbols = ["AAPL", "GOOGL", "MSFT", "TSLA", "AMZN"]

    price_data = []
    for symbol in symbols:
        base_price = random.uniform(100, 3000)
        for date in dates:
            # Add some random variation to prices
            variation = random.uniform(-0.05, 0.05)
            price = base_price * (1 + variation)
            price_data.append(
                {"Date": date, "Symbol": symbol, "Price": round(price, 2)}
            )
            base_price = price  # Use previous price as base for next day

    return pd.DataFrame(price_data)


def main():
    """Main Streamlit application"""
    st.title("📈 Portfolio Tracker Sandbox")
    st.markdown("---")

    # Sidebar
    st.sidebar.header("Settings")

    # Create sample data
    portfolio_df = create_sample_data()
    price_history_df = create_price_history()

    # Main content
    col1, col2, col3 = st.columns(3)

    with col1:
        total_invested = portfolio_df["Total Invested"].sum()
        st.metric("Total Invested", f"${total_invested:,.2f}")

    with col2:
        total_current = portfolio_df["Current Value"].sum()
        st.metric("Current Value", f"${total_current:,.2f}")

    with col3:
        total_gain_loss = portfolio_df["Gain/Loss"].sum()
        gain_loss_color = "green" if total_gain_loss >= 0 else "red"
        st.metric(
            "Total Gain/Loss",
            f"${total_gain_loss:,.2f}",
            delta=f"{total_gain_loss:,.2f}",
        )

    st.markdown("---")

    # Portfolio Table
    st.subheader("📊 Portfolio Overview")

    # Add color coding to the dataframe
    def color_gain_loss(val):
        if val > 0:
            return "background-color: lightgreen"
        elif val < 0:
            return "background-color: lightcoral"
        return ""

    styled_df = portfolio_df.style.applymap(
        color_gain_loss, subset=["Gain/Loss", "Gain/Loss %"]
    )
    st.dataframe(styled_df, use_container_width=True)

    # Charts
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("💰 Portfolio Allocation")

        # Pie chart of current values
        fig_pie = px.pie(
            portfolio_df,
            values="Current Value",
            names="Symbol",
            title="Portfolio Allocation by Stock",
        )
        fig_pie.update_traces(textposition="inside", textinfo="percent+label")
        st.plotly_chart(fig_pie, use_container_width=True)

    with col2:
        st.subheader("📈 Performance by Stock")

        # Bar chart of gain/loss percentages
        fig_bar = px.bar(
            portfolio_df,
            x="Symbol",
            y="Gain/Loss %",
            color="Gain/Loss %",
            color_continuous_scale=["red", "yellow", "green"],
            title="Gain/Loss Percentage by Stock",
        )
        fig_bar.update_layout(yaxis_title="Gain/Loss (%)")
        st.plotly_chart(fig_bar, use_container_width=True)

    # Price History Chart
    st.subheader("📊 Price History")

    # Filter by symbol
    selected_symbols = st.multiselect(
        "Select stocks to display:",
        options=price_history_df["Symbol"].unique(),
        default=price_history_df["Symbol"].unique()[:3],
    )

    if selected_symbols:
        filtered_df = price_history_df[
            price_history_df["Symbol"].isin(selected_symbols)
        ]

        fig_line = px.line(
            filtered_df,
            x="Date",
            y="Price",
            color="Symbol",
            title="Stock Price History",
            labels={"Price": "Price ($)", "Date": "Date"},
        )
        fig_line.update_layout(xaxis_title="Date", yaxis_title="Price ($)")
        st.plotly_chart(fig_line, use_container_width=True)

    # Interactive Features
    st.markdown("---")
    st.subheader("🎯 Interactive Features")

    col1, col2 = st.columns(2)

    with col1:
        st.write("**Add New Position**")
        new_symbol = st.text_input("Stock Symbol", placeholder="e.g., NVDA")
        new_shares = st.number_input("Number of Shares", min_value=1, value=10)
        new_price = st.number_input(
            "Purchase Price", min_value=0.01, value=100.0
        )

        if st.button("Add Position") and new_symbol:
            st.success(
                f"Added {new_shares} shares of {new_symbol} at ${new_price:.2f}"
            )

    with col2:
        st.write("**Portfolio Analysis**")

        # Sector analysis
        sector_analysis = (
            portfolio_df.groupby("Sector")["Current Value"].sum().reset_index()
        )
        fig_sector = px.pie(
            sector_analysis,
            values="Current Value",
            names="Sector",
            title="Portfolio by Sector",
        )
        st.plotly_chart(fig_sector, use_container_width=True)

    # Footer
    st.markdown("---")
    st.markdown(
        "*This is a sandbox environment with sample data for testing purposes.*"
    )


if __name__ == "__main__":
    main()
