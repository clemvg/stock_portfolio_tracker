# News API Client

A generic Python client for retrieving news via the NewsAPI with configurable parameters. Supports both top headlines and everything endpoints.

## Features

- **Generic API Client**: Supports both `top_headlines` and `everything` endpoints
- **Configurable Parameters**: All NewsAPI parameters are supported and configurable
- **Structured Data**: Returns well-structured data classes instead of raw dictionaries
- **Environment Variable Support**: Reads API key from `API_NEWS_KEY` environment variable
- **Error Handling**: Comprehensive error handling with meaningful error messages
- **Type Hints**: Full type annotations for better IDE support

## Installation

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

2. Set up your environment variables:
Create a `.env` file in your project root:
```env
API_NEWS_KEY=your_news_api_key_here
```

## Quick Start

### Basic Usage

```python
from app.api.news_client import get_news

# Get top business headlines
headlines = get_news(
    endpoint='top_headlines',
    category='business',
    country='us',
    page_size=5
)

# Search for articles about a specific topic
articles = get_news(
    endpoint='everything',
    q='artificial intelligence',
    language='en',
    sort_by='publishedAt'
)
```

### Using the Client Class

```python
from app.api.news_client import NewsAPIClient

# Create client instance
client = NewsAPIClient()

# Get top headlines
headlines = client.get_top_headlines(
    category='technology',
    country='us'
)

# Get all articles
articles = client.get_everything(
    q='stock market',
    from_param='2024-01-01',
    to='2024-01-31'
)

# Get available sources
sources = client.get_sources(category='business')
```

## API Reference

### NewsAPIClient Class

#### Constructor
```python
NewsAPIClient(api_key: Optional[str] = None)
```
- `api_key`: API key for NewsAPI. If not provided, reads from `API_NEWS_KEY` env var.

#### Methods

##### get_top_headlines()
```python
get_top_headlines(
    q: Optional[str] = None,
    sources: Optional[str] = None,
    category: Optional[str] = None,
    language: str = 'en',
    country: Optional[str] = None,
    page_size: int = 20,
    page: int = 1
) -> NewsResponse
```

**Parameters:**
- `q`: Keywords or phrase to search for
- `sources`: Comma-separated string of news source identifiers
- `category`: Category of headlines (business, entertainment, general, health, science, sports, technology)
- `language`: Language of articles (default: 'en')
- `country`: 2-letter ISO 3166-1 country code (us, gb, etc.)
- `page_size`: Number of results per page (max 100)
- `page`: Page number for pagination

**Note:** You can't mix `sources` param with `country` or `category` params.

##### get_everything()
```python
get_everything(
    q: Optional[str] = None,
    sources: Optional[str] = None,
    domains: Optional[str] = None,
    from_param: Optional[Union[str, date, datetime]] = None,
    to: Optional[Union[str, date, datetime]] = None,
    language: str = 'en',
    sort_by: str = 'relevancy',
    page_size: int = 20,
    page: int = 1
) -> NewsResponse
```

**Parameters:**
- `q`: Keywords or phrase to search for
- `sources`: Comma-separated string of news source identifiers
- `domains`: Comma-separated string of domains to restrict the search to
- `from_param`: Start date for articles (YYYY-MM-DD format or date/datetime object)
- `to`: End date for articles (YYYY-MM-DD format or date/datetime object)
- `language`: Language of articles (default: 'en')
- `sort_by`: Sort method (relevancy, popularity, publishedAt)
- `page_size`: Number of results per page (max 100)
- `page`: Page number for pagination

##### get_sources()
```python
get_sources(
    category: Optional[str] = None,
    language: str = 'en',
    country: Optional[str] = None
) -> Dict
```

**Parameters:**
- `category`: Category of sources (business, entertainment, general, health, science, sports, technology)
- `language`: Language of sources (default: 'en')
- `country`: 2-letter ISO 3166-1 country code

### Convenience Function

#### get_news()
```python
get_news(
    endpoint: str = 'top_headlines',
    **kwargs
) -> NewsResponse
```

**Parameters:**
- `endpoint`: Either 'top_headlines' or 'everything'
- `**kwargs`: Parameters to pass to the respective endpoint method

### Data Classes

#### NewsArticle
```python
@dataclass
class NewsArticle:
    source_id: str
    source_name: str
    author: Optional[str]
    title: str
    description: Optional[str]
    url: str
    url_to_image: Optional[str]
    published_at: str
    content: Optional[str]
```

#### NewsResponse
```python
@dataclass
class NewsResponse:
    status: str
    total_results: int
    articles: List[NewsArticle]
```

## Examples

### Get Business Headlines
```python
headlines = get_news(
    endpoint='top_headlines',
    category='business',
    country='us',
    page_size=10
)

print(f"Found {headlines.total_results} business headlines")
for article in headlines.articles:
    print(f"- {article.title} ({article.source_name})")
```

### Search for Articles
```python
articles = get_news(
    endpoint='everything',
    q='bitcoin OR cryptocurrency',
    language='en',
    sort_by='publishedAt',
    page_size=5
)

for article in articles.articles:
    print(f"- {article.title}")
    print(f"  Published: {article.published_at}")
    print(f"  URL: {article.url}")
```

### Date Range Search
```python
from datetime import datetime, timedelta

end_date = datetime.now()
start_date = end_date - timedelta(days=7)

articles = get_news(
    endpoint='everything',
    q='finance',
    from_param=start_date,
    to=end_date,
    language='en'
)
```

### Get Sources
```python
client = NewsAPIClient()
sources = client.get_sources(category='business')

for source in sources['sources']:
    print(f"- {source['name']} ({source['id']})")
```

## Error Handling

The client includes comprehensive error handling:

```python
try:
    articles = get_news(endpoint='top_headlines', category='business')
except Exception as e:
    print(f"Error fetching news: {e}")
```

Common error scenarios:
- Missing API key
- Invalid parameters
- Network errors
- API rate limiting

## Running Examples

To run the example script:

```bash
python examples/news_example.py
```

Make sure you have set the `API_NEWS_KEY` environment variable before running the examples.

## API Documentation

For complete API documentation, visit: https://newsapi.org/docs

## License

This project is part of the stock portfolio tracker application. 