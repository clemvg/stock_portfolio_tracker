#!/usr/bin/env python3
"""
Google News Sandbox for Portfolio Tracker
Test news retrieval and sentiment analysis for stocks
Deprecated: Google News is not working anymore
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime, timedelta
import time
import json
from typing import Dict, List, Optional, Tuple
import re
from urllib.parse import quote_plus
import warnings

warnings.filterwarnings("ignore")


class GoogleNewsSandbox:
    def __init__(self):
        self.base_url = "https://news.google.com"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)

    def search_news(self, query: str, days: int = 7) -> List[Dict]:
        """Search for news articles using Google News"""
        try:
            # Format query for Google News
            formatted_query = quote_plus(query)

            # Google News search URL
            search_url = f"{self.base_url}/search?q={formatted_query}&hl=en-US&gl=US&ceid=US:en"

            print(f"🔍 Searching for: {query}")

            # Make request
            response = self.session.get(search_url, timeout=10)
            response.raise_for_status()

            # Parse HTML
            soup = BeautifulSoup(response.content, "html.parser")

            # Extract articles
            articles = []
            article_elements = soup.find_all("article")

            for article in article_elements[:10]:  # Limit to 10 articles
                try:
                    # Extract title
                    title_element = article.find("h3") or article.find("h4")
                    title = (
                        title_element.get_text().strip()
                        if title_element
                        else "No title"
                    )

                    # Extract link
                    link_element = article.find("a")
                    link = link_element.get("href") if link_element else ""
                    if link and link.startswith("./"):
                        link = self.base_url + link[1:]

                    # Extract source
                    source_element = article.find("time") or article.find(
                        "span"
                    )
                    source = (
                        source_element.get_text().strip()
                        if source_element
                        else "Unknown source"
                    )

                    # Extract time
                    time_element = article.find("time")
                    time_str = (
                        time_element.get("datetime") if time_element else ""
                    )

                    articles.append(
                        {
                            "title": title,
                            "link": link,
                            "source": source,
                            "time": time_str,
                            "query": query,
                        }
                    )

                except Exception as e:
                    print(f"⚠️  Error parsing article: {e}")
                    continue

            print(f"✅ Found {len(articles)} articles for '{query}'")
            return articles

        except Exception as e:
            print(f"❌ Error searching news for '{query}': {e}")
            return []

    def get_stock_news(
        self, symbol: str, company_name: str = "", days: int = 7
    ) -> List[Dict]:
        """Get news for a specific stock"""
        # Create search queries
        queries = [symbol]
        if company_name:
            queries.append(company_name)
            queries.append(f"{symbol} {company_name}")

        all_articles = []
        for query in queries:
            articles = self.search_news(query, days)
            all_articles.extend(articles)
            time.sleep(1)  # Be nice to Google

        # Remove duplicates based on title
        seen_titles = set()
        unique_articles = []
        for article in all_articles:
            if article["title"] not in seen_titles:
                seen_titles.add(article["title"])
                unique_articles.append(article)

        return unique_articles[:15]  # Limit to 15 unique articles

    def analyze_sentiment(self, text: str) -> Dict:
        """Simple sentiment analysis (basic implementation)"""
        # Simple keyword-based sentiment analysis
        positive_words = [
            "up",
            "rise",
            "gain",
            "positive",
            "growth",
            "profit",
            "earnings",
            "beat",
            "strong",
            "bullish",
            "surge",
            "rally",
            "higher",
            "increase",
            "success",
        ]

        negative_words = [
            "down",
            "fall",
            "drop",
            "negative",
            "loss",
            "decline",
            "miss",
            "weak",
            "bearish",
            "crash",
            "lower",
            "decrease",
            "failure",
            "risk",
            "concern",
        ]

        text_lower = text.lower()

        positive_count = sum(1 for word in positive_words if word in text_lower)
        negative_count = sum(1 for word in negative_words if word in text_lower)

        if positive_count > negative_count:
            sentiment = "positive"
            score = positive_count / (positive_count + negative_count + 1)
        elif negative_count > positive_count:
            sentiment = "negative"
            score = negative_count / (positive_count + negative_count + 1)
        else:
            sentiment = "neutral"
            score = 0.5

        return {
            "sentiment": sentiment,
            "score": round(score, 3),
            "positive_words": positive_count,
            "negative_words": negative_count,
        }

    def analyze_news_sentiment(self, articles: List[Dict]) -> pd.DataFrame:
        """Analyze sentiment for a list of articles"""
        if not articles:
            return pd.DataFrame()

        analyzed_articles = []
        for article in articles:
            sentiment = self.analyze_sentiment(article["title"])

            analyzed_article = {
                "title": article["title"],
                "source": article["source"],
                "link": article["link"],
                "sentiment": sentiment["sentiment"],
                "sentiment_score": sentiment["score"],
                "positive_words": sentiment["positive_words"],
                "negative_words": sentiment["negative_words"],
                "query": article["query"],
            }
            analyzed_articles.append(analyzed_article)

        return pd.DataFrame(analyzed_articles)

    def get_market_news(self, days: int = 7) -> List[Dict]:
        """Get general market news"""
        market_queries = [
            "stock market",
            "Wall Street",
            "S&P 500",
            "NASDAQ",
            "Dow Jones",
            "market news",
            "trading news",
        ]

        all_market_news = []
        for query in market_queries[:3]:  # Limit to avoid rate limits
            articles = self.search_news(query, days)
            all_market_news.extend(articles)
            time.sleep(1)

        return all_market_news[:10]  # Limit to 10 articles

    def create_news_summary(self, symbol: str, company_name: str = "") -> Dict:
        """Create a comprehensive news summary for a stock"""
        print(f"\n📰 Creating news summary for {symbol}...")

        # Get stock-specific news
        stock_news = self.get_stock_news(symbol, company_name)

        if not stock_news:
            return {"error": f"No news found for {symbol}"}

        # Analyze sentiment
        news_df = self.analyze_news_sentiment(stock_news)

        # Calculate summary statistics
        sentiment_counts = news_df["sentiment"].value_counts()
        avg_sentiment_score = news_df["sentiment_score"].mean()

        # Get recent headlines
        recent_headlines = news_df.head(5)[
            ["title", "sentiment", "source"]
        ].to_dict("records")

        summary = {
            "symbol": symbol,
            "company_name": company_name,
            "total_articles": len(news_df),
            "sentiment_distribution": sentiment_counts.to_dict(),
            "average_sentiment_score": round(avg_sentiment_score, 3),
            "overall_sentiment": sentiment_counts.index[0]
            if len(sentiment_counts) > 0
            else "neutral",
            "recent_headlines": recent_headlines,
            "all_articles": news_df.to_dict("records"),
        }

        return summary

    def compare_stock_news(
        self, symbols: List[str], company_names: List[str] = None
    ) -> pd.DataFrame:
        """Compare news sentiment across multiple stocks"""
        print(f"\n📊 Comparing news sentiment for {len(symbols)} stocks...")

        if company_names is None:
            company_names = [""] * len(symbols)

        comparison_data = []

        for symbol, company_name in zip(symbols, company_names):
            summary = self.create_news_summary(symbol, company_name)

            if "error" not in summary:
                comparison_data.append(
                    {
                        "Symbol": symbol,
                        "Company": company_name,
                        "Total Articles": summary["total_articles"],
                        "Overall Sentiment": summary["overall_sentiment"],
                        "Avg Sentiment Score": summary[
                            "average_sentiment_score"
                        ],
                        "Positive Articles": summary[
                            "sentiment_distribution"
                        ].get("positive", 0),
                        "Negative Articles": summary[
                            "sentiment_distribution"
                        ].get("negative", 0),
                        "Neutral Articles": summary[
                            "sentiment_distribution"
                        ].get("neutral", 0),
                    }
                )

            time.sleep(2)  # Be nice to Google

        return pd.DataFrame(comparison_data)

    def save_news_data(self, data: Dict, filename: str = None):
        """Save news data to JSON file"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"news_data_{timestamp}.json"

        try:
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False, default=str)
            print(f"✅ Saved news data to {filename}")
        except Exception as e:
            print(f"❌ Error saving data: {e}")

    def test_all_features(self):
        """Test all sandbox features"""
        print("🚀 Google News Sandbox - Testing All Features")
        print("=" * 60)

        # Test stocks
        test_stocks = [
            ("AAPL", "Apple Inc."),
            ("GOOGL", "Alphabet Inc."),
            ("MSFT", "Microsoft Corporation"),
        ]

        # 1. Test basic news search
        print("\n1. 🔍 Testing Basic News Search:")
        test_query = "Apple stock"
        articles = self.search_news(test_query)
        if articles:
            print(f"   Found {len(articles)} articles for '{test_query}'")
            print(f"   Sample: {articles[0]['title'][:50]}...")

        # 2. Test stock-specific news
        print("\n2. 📰 Testing Stock-Specific News:")
        for symbol, company in test_stocks[
            :2
        ]:  # Test first 2 to avoid rate limits
            stock_news = self.get_stock_news(symbol, company)
            print(f"   {symbol}: {len(stock_news)} articles found")

        # 3. Test sentiment analysis
        print("\n3. 📊 Testing Sentiment Analysis:")
        sample_articles = [
            {"title": "Apple stock surges on strong earnings report"},
            {"title": "Apple stock drops on weak iPhone sales"},
            {"title": "Apple announces new product line"},
        ]

        for article in sample_articles:
            sentiment = self.analyze_sentiment(article["title"])
            print(
                f"   '{article['title']}' -> {sentiment['sentiment']} (score: {sentiment['score']})"
            )

        # 4. Test news summary
        print("\n4. 📋 Testing News Summary:")
        summary = self.create_news_summary("AAPL", "Apple Inc.")
        if "error" not in summary:
            print(
                f"   AAPL: {summary['total_articles']} articles, {summary['overall_sentiment']} sentiment"
            )

        # 5. Test comparison
        print("\n5. 📈 Testing Stock Comparison:")
        comparison = self.compare_stock_news(
            ["AAPL", "GOOGL"], ["Apple Inc.", "Alphabet Inc."]
        )
        if not comparison.empty:
            print(
                comparison[
                    [
                        "Symbol",
                        "Total Articles",
                        "Overall Sentiment",
                        "Avg Sentiment Score",
                    ]
                ].to_string(index=False)
            )

        # 6. Test market news
        print("\n6. 🌐 Testing Market News:")
        market_news = self.get_market_news()
        print(f"   Found {len(market_news)} market news articles")

        # 7. Save sample data
        print("\n7. 💾 Testing Data Export:")
        if "error" not in summary:
            self.save_news_data(summary, "sample_news_data.json")

        print("\n✅ All Google News tests completed!")


def main():
    """Main function to run Google News sandbox tests"""
    sandbox = GoogleNewsSandbox()
    sandbox.test_all_features()


if __name__ == "__main__":
    main()
