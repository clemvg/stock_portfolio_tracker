# Google News Sandbox

Test news retrieval and sentiment analysis for stocks using Google News.

## What to Test

- News article retrieval from Google News
- Stock-specific news searches
- Basic sentiment analysis
- News comparison across stocks
- Market news aggregation
- Data export and storage

## Commands to Run

```bash
# Navigate to sandbox directory
cd sandboxes/news

# Install dependencies (from main repo)
pip install -r ../../requirements.txt

# Run the Google News sandbox
python news_sandbox.py

# Test specific features
python -c "
from news_sandbox import GoogleNewsSandbox
sandbox = GoogleNewsSandbox()
articles = sandbox.search_news('AAPL stock')
print(f'Found {len(articles)} articles')
"
```

## Expected Output

You should see:
- 🔍 News search results for various queries
- 📰 Stock-specific news articles
- 📊 Sentiment analysis results
- 📋 News summaries with sentiment distribution
- 📈 Stock comparison tables
- 🌐 Market news articles
- 💾 JSON data export

## Features to Test

1. **News Search**: Search for any topic or stock
2. **Stock News**: Get news specific to stock symbols
3. **Sentiment Analysis**: Basic keyword-based sentiment scoring
4. **News Summary**: Comprehensive analysis of news for a stock
5. **Stock Comparison**: Compare news sentiment across multiple stocks
6. **Market News**: Get general market and trading news
7. **Data Export**: Save news data to JSON files

## Sample Data Generated

- `sample_news_data.json` - News summary data
- `news_data_YYYYMMDD_HHMMSS.json` - Timestamped news data
- Console output with sentiment analysis results

## Play Around Ideas

1. Test with different stock symbols
2. Modify search queries and time periods
3. Improve sentiment analysis with more keywords
4. Add news categorization (earnings, product launches, etc.)
5. Create news alerts for specific keywords
6. Add news source filtering
7. Implement more sophisticated sentiment analysis
8. Create news trend analysis over time
9. Add news impact scoring on stock prices

## Troubleshooting

- **Rate Limits**: Google may block requests if too frequent, add delays
- **No Results**: Some queries might not return results, try different terms
- **Network Issues**: Check internet connection
- **Parsing Errors**: Google News structure may change, update selectors
- **Blocked Requests**: Use VPN or different IP if blocked

## Limitations

- **Web Scraping**: Relies on Google News HTML structure
- **Rate Limits**: Google may limit frequent requests
- **Basic Sentiment**: Uses simple keyword matching
- **No API**: Not using official Google News API
- **Structure Changes**: Google News layout may change

## Alternative Approaches

1. Use official news APIs (NewsAPI, Alpha Vantage News)
2. Implement more sophisticated NLP for sentiment
3. Add news categorization and filtering
4. Create news impact correlation with stock prices
5. Build news alert system 