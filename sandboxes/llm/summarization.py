from huggingface_hub import InferenceClient
import os
from dotenv import load_dotenv

load_dotenv()
# https://huggingface.co/facebook/bart-large-cnn
# https://huggingface.co/models?pipeline_tag=summarization&sort=trending
# longer inference time

def get_bart_summary(
    text: str,
    # max_length: int = 142, # TODO params doe not work
    # min_length: int = 56, # TODO
):
    """
    Alternative method using text_generation with proper task specification.
    """
    try:
        client = InferenceClient(
            model="facebook/bart-large-cnn",
            token=os.environ["HUGGINGFACE_TOKEN"],
        )
        
        # Format the input for summarization
        inputs = f"summarize: {text}"
        
        result = client.summarization(
            inputs,
            # max_new_tokens=max_length,
            # min_length=min_length,
        )
        
        return result
        
    except Exception as e:
        print(f"Error making summarization request: {e}")
        return None
    
    
# Example usage
if __name__ == "__main__":
    # Sample text to summarize
    sample_text = """
    The United States has a rich history of innovation and technological advancement. 
    From the invention of the telephone by Alexander Graham Bell to the development 
    of the internet, American inventors and scientists have consistently pushed the 
    boundaries of what's possible. The country's emphasis on research and development, 
    combined with a culture that encourages entrepreneurship, has led to breakthrough 
    discoveries in fields ranging from medicine to space exploration. Today, American 
    companies continue to lead in areas such as artificial intelligence, biotechnology, 
    and renewable energy, ensuring that the nation remains at the forefront of global 
    innovation.
    """

    # Get summary
    summary = get_bart_summary(sample_text)
    if summary:
        print("Summary:", summary)
    else:
        print("Failed to generate summary")