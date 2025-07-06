"""
News API Client

A generic client for retrieving news via the NewsAPI with configurable parameters.
Supports both top headlines and everything endpoints.
"""

import os
from typing import Dict, List, Optional, Union
from datetime import datetime, date
from dataclasses import dataclass
from newsapi import NewsApiClient
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


@dataclass # no BaseModel pydantic?
class NewsArticle:
    """Data class representing a news article."""

    source_id: str
    source_name: str
    author: Optional[str]
    title: str
    description: Optional[str]
    url: str
    url_to_image: Optional[str]
    published_at: str
    content: Optional[str]


@dataclass
class NewsResponse:
    """Data class representing a news API response."""

    status: str
    total_results: int
    articles: List[NewsArticle]


class NewsAPIClient:
    """
    Generic News API Client for retrieving news articles.

    Supports both top headlines and everything endpoints with configurable parameters.
    """

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the News API client.

        Args:
            api_key: API key for NewsAPI. If not provided, reads from API_NEWS_KEY env var.
        """
        if api_key is None:
            api_key = os.getenv("API_NEWS_KEY")
            if not api_key:
                raise ValueError(
                    "API key not found. Set API_NEWS_KEY environment variable or pass api_key parameter."
                )

        self.client = NewsApiClient(api_key=api_key)

    def get_top_headlines(
        self,
        q: Optional[str] = None,
        sources: Optional[str] = None,
        category: Optional[str] = None,
        language: str = "en",
        country: Optional[str] = None,
        page_size: int = 20,
        page: int = 1,
    ) -> NewsResponse:
        """
        Get top headlines from NewsAPI.

        Args:
            q: Keywords or phrase to search for
            sources: Comma-separated string of news source identifiers
            category: Category of headlines (business, entertainment, general, health, science, sports, technology)
            language: Language of articles (default: 'en')
            country: 2-letter ISO 3166-1 country code (us, gb, etc.)
            page_size: Number of results per page (max 100)
            page: Page number for pagination

        Returns:
            NewsResponse object containing articles and metadata

        Note: You can't mix sources param with country or category params.
        """
        try:
            response = self.client.get_top_headlines(
                q=q,
                sources=sources,
                category=category,
                language=language,
                country=country,
                page_size=page_size,
                page=page,
            )

            return self._parse_response(response)

        except Exception as e:
            raise Exception(f"Error fetching top headlines: {str(e)}")

    def get_everything(
        self,
        q: Optional[str] = None,
        sources: Optional[str] = None,
        domains: Optional[str] = None,
        from_param: Optional[Union[str, date, datetime]] = None,
        to: Optional[Union[str, date, datetime]] = None,
        language: str = "en",
        sort_by: str = "relevancy",
        page_size: int = 20,
        page: int = 1,
    ) -> NewsResponse:
        """
        Get all articles from NewsAPI.

        Args:
            q: Keywords or phrase to search for
            sources: Comma-separated string of news source identifiers
            domains: Comma-separated string of domains to restrict the search to
            from_param: Start date for articles (YYYY-MM-DD format or date/datetime object)
            to: End date for articles (YYYY-MM-DD format or date/datetime object)
            language: Language of articles (default: 'en')
            sort_by: Sort method (relevancy, popularity, publishedAt)
            page_size: Number of results per page (max 100)
            page: Page number for pagination

        Returns:
            NewsResponse object containing articles and metadata
        """
        try:
            # Convert date objects to string format
            if isinstance(from_param, (date, datetime)):
                from_param = from_param.strftime("%Y-%m-%d")
            if isinstance(to, (date, datetime)):
                to = to.strftime("%Y-%m-%d")

            response = self.client.get_everything(
                q=q,
                sources=sources,
                domains=domains,
                from_param=from_param,
                to=to,
                language=language,
                sort_by=sort_by,
                page_size=page_size,
                page=page,
            )

            return self._parse_response(response)

        except Exception as e:
            raise Exception(f"Error fetching articles: {str(e)}")

    def get_sources(
        self,
        category: Optional[str] = None,
        language: str = "en",
        country: Optional[str] = None,
    ) -> Dict:
        """
        Get available news sources.

        Args:
            category: Category of sources (business, entertainment, general, health, science, sports, technology)
            language: Language of sources (default: 'en')
            country: 2-letter ISO 3166-1 country code

        Returns:
            Dictionary containing sources information
        """
        try:
            return self.client.get_sources(
                category=category, language=language, country=country
            )
        except Exception as e:
            raise Exception(f"Error fetching sources: {str(e)}")

    def _parse_response(self, response: Dict) -> NewsResponse:
        """
        Parse the raw API response into a structured NewsResponse object.

        Args:
            response: Raw response from NewsAPI

        Returns:
            NewsResponse object with parsed articles
        """
        articles = []

        for article_data in response.get("articles", []):
            source = article_data.get("source", {})
            article = NewsArticle(
                source_id=source.get("id", ""),
                source_name=source.get("name", ""),
                author=article_data.get("author"),
                title=article_data.get("title", ""),
                description=article_data.get("description"),
                url=article_data.get("url", ""),
                url_to_image=article_data.get("urlToImage"),
                published_at=article_data.get("publishedAt", ""),
                content=article_data.get("content"),
            )
            articles.append(article)

        return NewsResponse(
            status=response.get("status", ""),
            total_results=response.get("totalResults", 0),
            articles=articles,
        )


def get_news(endpoint: str = "top_headlines", **kwargs) -> NewsResponse:
    """
    Convenience function to get news articles.

    Args:
        endpoint: Either 'top_headlines' or 'everything'
        **kwargs: Parameters to pass to the respective endpoint method

    Returns:
        NewsResponse object containing articles and metadata
    """
    client = NewsAPIClient()

    if endpoint == "top_headlines":
        return client.get_top_headlines(**kwargs)
    elif endpoint == "everything":
        return client.get_everything(**kwargs)
    else:
        raise ValueError(
            "endpoint must be either 'top_headlines' or 'everything'"
        )


# Example usage - two examples
if __name__ == "__main__":
    # Example 1: Get top business headlines
    try:
        headlines = get_news(
            endpoint="top_headlines",
            category="business",
            country="us",
            page_size=5,
        )
        print(f"Found {headlines.total_results} business headlines")
        for article in headlines.articles:
            print(f"- {article.title} ({article.source_name})")
    except Exception as e:
        print(f"Error: {e}")

    # Example 2: Search for articles about a specific topic
    try:
        articles = get_news(
            endpoint="everything",
            q="Apple stock price",
            language="en",
            sort_by="publishedAt",
            page_size=3,
        )
        print(f"\nFound {articles.total_results} articles about AI")
        for article in articles.articles:
            print(f"- {article.title} ({article.source_name})")
    except Exception as e:
        print(f"Error: {e}")
