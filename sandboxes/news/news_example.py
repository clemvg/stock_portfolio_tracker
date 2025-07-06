#!/usr/bin/env python3
"""
Example USAGE of the News API Client

This script demonstrates how to use the generic news API client
to retrieve news articles with different parameters and endpoints.
"""

import sys
import os
from datetime import datetime, timedelta

# Add the app directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "app"))

from news_client import NewsAPIClient, get_news # in dir


def example_top_headlines():
    """Example: Get top headlines with different parameters."""
    print("=== Top Headlines Examples ===\n")

    # Example 1: Business headlines from US
    print("1. Business headlines from US:")
    try:
        headlines = get_news(
            endpoint="top_headlines",
            category="business", # business, technology, science, health, entertainment, general, sports
            country="us", # loop 
            page_size=3, # 100 max
        )
        print(f"Found {headlines.total_results} business headlines")
        for article in headlines.articles:
            print(f"  - {article.title}")
            print(f"    Source: {article.source_name}")
            print(f"    Published: {article.published_at}")
            print()
    except Exception as e:
        print(f"Error: {e}\n")

    # Example 2: Technology headlines
    print("2. Technology headlines:")
    try:
        headlines = get_news(
            endpoint="top_headlines",
            category="technology",
            country="us",
            page_size=3,
        )
        print(f"Found {headlines.total_results} technology headlines")
        for article in headlines.articles:
            print(f"  - {article.title}")
            print(f"    Source: {article.source_name}")
            print()
    except Exception as e:
        print(f"Error: {e}\n")

    # Example 3: Search for specific topic in headlines
    print("3. Headlines about 'AI' or 'artificial intelligence':")
    try:
        headlines = get_news(
            endpoint="top_headlines",
            q="AI OR artificial intelligence",
            language="en",
            page_size=3,
        )
        print(f"Found {headlines.total_results} AI-related headlines")
        for article in headlines.articles:
            print(f"  - {article.title}")
            print(f"    Source: {article.source_name}")
            print()
    except Exception as e:
        print(f"Error: {e}\n")


def example_everything():
    """Example: Get all articles with different parameters."""
    print("=== Everything Endpoint Examples ===\n")

    # Example 1: Search for articles about a specific topic
    print("1. Articles about 'stock market':")
    try:
        articles = get_news(
            endpoint="everything",
            q="stock market",
            language="en",
            sort_by="publishedAt",
            page_size=3,
        )
        print(f"Found {articles.total_results} articles about stock market")
        for article in articles.articles:
            print(f"  - {article.title}")
            print(f"    Source: {article.source_name}")
            print(f"    Published: {article.published_at}")
            print(f"    URL: {article.url}")
            print()
    except Exception as e:
        print(f"Error: {e}\n")

    # Example 2: Articles from specific domains
    print("2. Articles from specific domains (BBC and TechCrunch):")
    try:
        articles = get_news(
            endpoint="everything",
            domains="bbc.co.uk,techcrunch.com",
            language="en",
            sort_by="relevancy",
            page_size=3,
        )
        print(f"Found {articles.total_results} articles from specified domains")
        for article in articles.articles:
            print(f"  - {article.title}")
            print(f"    Source: {article.source_name}")
            print()
    except Exception as e:
        print(f"Error: {e}\n")

    # Example 3: Articles from a specific date range
    print("3. Articles from the last 7 days about 'finance':")
    try:
        end_date = datetime.now()
        start_date = end_date - timedelta(days=7)

        articles = get_news(
            endpoint="everything",
            q="finance",
            from_param=start_date,
            to=end_date,
            language="en",
            sort_by="publishedAt",
            page_size=3,
        )
        print(
            f"Found {articles.total_results} finance articles from the last 7 days"
        )
        for article in articles.articles:
            print(f"  - {article.title}")
            print(f"    Source: {article.source_name}")
            print(f"    Published: {article.published_at}")
            print()
    except Exception as e:
        print(f"Error: {e}\n")


def example_sources():
    """Example: Get available news sources."""
    print("=== Sources Examples ===\n")

    client = NewsAPIClient()

    # Example 1: Get all sources
    print("1. All available sources:")
    try:
        sources = client.get_sources()
        print(f"Found {len(sources.get('sources', []))} sources")
        for source in sources.get("sources", [])[:5]:  # Show first 5
            print(f"  - {source.get('name')} ({source.get('id')})")
            print(f"    Category: {source.get('category')}")
            print(f"    Language: {source.get('language')}")
            print()
    except Exception as e:
        print(f"Error: {e}\n")

    # Example 2: Get business sources
    print("2. Business sources:")
    try:
        sources = client.get_sources(category="business")
        print(f"Found {len(sources.get('sources', []))} business sources")
        for source in sources.get("sources", [])[:3]:  # Show first 3
            print(f"  - {source.get('name')} ({source.get('id')})")
            print()
    except Exception as e:
        print(f"Error: {e}\n")


def example_advanced_usage():
    """Example: Advanced usage with the client class."""
    print("=== Advanced Usage Examples ===\n")

    # Create client instance
    client = NewsAPIClient()

    # Example: Get articles with complex filtering
    print("1. Complex search with multiple parameters:")
    try:
        articles = client.get_everything(
            q="(bitcoin OR cryptocurrency) AND (price OR market)",
            language="en",
            sort_by="popularity",
            page_size=5,
        )
        print(f"Found {articles.total_results} cryptocurrency articles")
        for article in articles.articles:
            print(f"  - {article.title}")
            print(f"    Author: {article.author or 'Unknown'}")
            print(f"    Description: {article.description or 'No description'}")
            print(f"    URL: {article.url}")
            print()
    except Exception as e:
        print(f"Error: {e}\n")


def main():
    """Run all examples."""
    print("News API Client Examples")
    print("=" * 50)
    print()

    # Check if API key is available
    if not os.getenv("API_NEWS_KEY"):
        print("Warning: API_NEWS_KEY environment variable not set.")
        print("Please set your NewsAPI key in the .env file:")
        print("API_NEWS_KEY=your_api_key_here")
        print()
        return

    example_top_headlines()
    example_everything()
    example_sources() # can filter on bloomberg for instance
    example_advanced_usage()

    print("Examples completed!")


if __name__ == "__main__":
    main()
