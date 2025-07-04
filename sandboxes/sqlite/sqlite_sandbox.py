#!/usr/bin/env python3
"""
SQLite Sandbox for Portfolio Tracker
Test basic database operations and schema
"""

import sqlite3
import os
from datetime import datetime
from typing import List, Dict, Any


class SQLiteSandbox:
    def __init__(self, db_path: str = "portfolio_test.db"):
        self.db_path = db_path
        self.conn = None
        self.cursor = None

    def connect(self):
        """Connect to SQLite database"""
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()
        print(f"✅ Connected to {self.db_path}")

    def disconnect(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
            print("✅ Database connection closed")

    def create_tables(self):
        """Create basic tables for portfolio tracking"""
        tables = [
            """
            CREATE TABLE IF NOT EXISTS stocks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                symbol TEXT UNIQUE NOT NULL,
                company_name TEXT,
                sector TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS portfolio (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                stock_id INTEGER,
                shares REAL NOT NULL,
                purchase_price REAL NOT NULL,
                purchase_date DATE NOT NULL,
                FOREIGN KEY (stock_id) REFERENCES stocks (id)
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS prices (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                stock_id INTEGER,
                price REAL NOT NULL,
                date DATE NOT NULL,
                FOREIGN KEY (stock_id) REFERENCES stocks (id)
            )
            """,
        ]

        for table_sql in tables:
            self.cursor.execute(table_sql)

        self.conn.commit()
        print("✅ Tables created successfully")

    def insert_sample_data(self):
        """Insert sample data for testing"""
        # Insert sample stocks
        stocks_data = [
            ("AAPL", "Apple Inc.", "Technology"),
            ("GOOGL", "Alphabet Inc.", "Technology"),
            ("MSFT", "Microsoft Corporation", "Technology"),
            ("TSLA", "Tesla Inc.", "Automotive"),
            ("AMZN", "Amazon.com Inc.", "Consumer Discretionary"),
        ]

        for symbol, name, sector in stocks_data:
            try:
                self.cursor.execute(
                    "INSERT INTO stocks (symbol, company_name, sector) VALUES (?, ?, ?)",
                    (symbol, name, sector),
                )
            except sqlite3.IntegrityError:
                print(f"⚠️  Stock {symbol} already exists")

        # Insert sample portfolio entries
        portfolio_data = [
            (1, 10, 150.00, "2024-01-15"),
            (2, 5, 2800.00, "2024-01-20"),
            (3, 8, 380.00, "2024-02-01"),
            (4, 20, 200.00, "2024-02-10"),
            (5, 15, 3300.00, "2024-02-15"),
        ]

        for stock_id, shares, price, date in portfolio_data:
            self.cursor.execute(
                "INSERT INTO portfolio (stock_id, shares, purchase_price, purchase_date) VALUES (?, ?, ?, ?)",
                (stock_id, shares, price, date),
            )

        # Insert sample prices
        prices_data = [
            (1, 155.00, "2024-03-01"),
            (2, 2850.00, "2024-03-01"),
            (3, 395.00, "2024-03-01"),
            (4, 210.00, "2024-03-01"),
            (5, 3400.00, "2024-03-01"),
        ]

        for stock_id, price, date in prices_data:
            self.cursor.execute(
                "INSERT INTO prices (stock_id, price, date) VALUES (?, ?, ?)",
                (stock_id, price, date),
            )

        self.conn.commit()
        print("✅ Sample data inserted successfully")

    def test_queries(self):
        """Test various database queries"""
        print("\n📊 Testing Database Queries:")

        # Get all stocks
        print("\n1. All stocks:")
        self.cursor.execute("SELECT * FROM stocks")
        stocks = self.cursor.fetchall()
        for stock in stocks:
            print(f"   {stock[1]} - {stock[2]} ({stock[3]})")

        # Get portfolio summary
        print("\n2. Portfolio summary:")
        self.cursor.execute("""
            SELECT s.symbol, s.company_name, p.shares, p.purchase_price, 
                   (p.shares * p.purchase_price) as total_invested
            FROM portfolio p
            JOIN stocks s ON p.stock_id = s.id
        """)
        portfolio = self.cursor.fetchall()
        for item in portfolio:
            print(
                f"   {item[0]} ({item[1]}): {item[2]} shares @ ${item[3]:.2f} = ${item[4]:.2f}"
            )

        # Get current prices
        print("\n3. Current prices:")
        self.cursor.execute("""
            SELECT s.symbol, pr.price, pr.date
            FROM prices pr
            JOIN stocks s ON pr.stock_id = s.id
            WHERE pr.date = (SELECT MAX(date) FROM prices WHERE stock_id = pr.stock_id)
        """)
        prices = self.cursor.fetchall()
        for price in prices:
            print(f"   {price[0]}: ${price[1]:.2f} ({price[2]})")

        # Calculate portfolio value
        print("\n4. Portfolio value calculation:")
        self.cursor.execute("""
            SELECT s.symbol, p.shares, pr.price, 
                   (p.shares * pr.price) as current_value,
                   (p.shares * p.purchase_price) as invested_value,
                   ((p.shares * pr.price) - (p.shares * p.purchase_price)) as gain_loss
            FROM portfolio p
            JOIN stocks s ON p.stock_id = s.id
            JOIN prices pr ON s.id = pr.stock_id
            WHERE pr.date = (SELECT MAX(date) FROM prices WHERE stock_id = pr.stock_id)
        """)
        portfolio_value = self.cursor.fetchall()
        total_invested = 0
        total_current = 0

        for item in portfolio_value:
            symbol, shares, price, current_val, invested_val, gain_loss = item
            total_invested += invested_val
            total_current += current_val
            print(
                f"   {symbol}: ${current_val:.2f} (Gain/Loss: ${gain_loss:.2f})"
            )

        print(f"\n   Total Invested: ${total_invested:.2f}")
        print(f"   Total Current Value: ${total_current:.2f}")
        print(f"   Total Gain/Loss: ${total_current - total_invested:.2f}")

    def cleanup(self):
        """Remove test database"""
        if os.path.exists(self.db_path):
            os.remove(self.db_path)
            print(f"✅ Cleaned up {self.db_path}")


def main():
    """Main function to run SQLite sandbox tests"""
    print("🚀 SQLite Sandbox - Portfolio Tracker Database Testing")
    print("=" * 60)

    sandbox = SQLiteSandbox()

    try:
        # Test database operations
        sandbox.connect()
        sandbox.create_tables()
        sandbox.insert_sample_data()
        sandbox.test_queries()

        print("\n✅ All SQLite tests completed successfully!")

    except Exception as e:
        print(f"❌ Error: {e}")

    finally:
        sandbox.disconnect()
        # Uncomment the next line to clean up the test database
        # sandbox.cleanup()


if __name__ == "__main__":
    main()
