# SQLite Sandbox

Test SQLite database operations for the portfolio tracker.

## What to Test

- Database connection and table creation
- Sample data insertion
- Portfolio queries and calculations
- Foreign key relationships

## Commands to Run

```bash
# Navigate to sandbox directory
cd sandboxes/sqlite

# Run the SQLite sandbox
python sqlite_sandbox.py

# Clean up test database (uncomment cleanup line in code)
# The script will create portfolio_test.db file
```

## Expected Output

You should see:
- ✅ Database connection success
- ✅ Tables created (stocks, portfolio, prices)
- ✅ Sample data inserted
- 📊 Query results showing:
  - All stocks in database
  - Portfolio summary with investments
  - Current prices
  - Portfolio value calculations with gains/losses

## Files Created

- `portfolio_test.db` - SQLite database file (will be created)
- `sqlite_sandbox.py` - Main test script

## Database Schema

- **stocks**: Stock symbols and company info
- **portfolio**: User's stock holdings
- **prices**: Historical price data

## Play Around Ideas

1. Add more stocks to the database
2. Modify portfolio entries
3. Add more price history
4. Create new queries for analysis
5. Test different date ranges 