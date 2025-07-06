# https://huggingface.co/mrm8488/distilroberta-finetuned-financial-news-sentiment-analysis
# mrm8488/distilroberta-finetuned-financial-news-sentiment-analysis

from huggingface_hub import InferenceClient
import os
from dotenv import load_dotenv

load_dotenv()

def get_financial_sentiment(
    text: str,
):
    """
    Alternative method using text_generation with proper task specification.
    """
    try:
        client = InferenceClient(
            model="mrm8488/distilroberta-finetuned-financial-news-sentiment-analysis",
            token=os.environ["HUGGINGFACE_TOKEN"],
        )

        # Format the input for summarization
        inputs = f"summarize: {text}"

        result = client.text_classification(
            inputs,
        )

        return result

    except Exception as e:
        print(f"Error making summarization request: {e}")
        return None


# Example usage
if __name__ == "__main__":
    # Sample text to summarize
    sample_text = """
    Apple Inc. (AAPL) reported a 20% decline in revenue for the second quarter, citing supply chain disruptions and weak demand for its products. The company's stock price fell by 10% in after-hours trading.
    """

    # Get summary
    sentiment = get_financial_sentiment(sample_text)
    if sentiment:
        # Get the most likely sentiment and its score
        print("Sentiment:", sentiment)
        top_sentiment = sentiment[0]
        print(f"Sentiment: {top_sentiment.label} (score: {top_sentiment.score:.2f})")
    else:
        print("Failed to get sentiment")
