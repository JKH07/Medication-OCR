import os
import time
import pathlib
from datetime import date
from dotenv import load_dotenv
import PIL.Image
from google import genai
from google.genai import types
from google.genai.errors import APIError

# Load environment variables from .env file
load_dotenv()

# Connection to LLM API
def client_creation():
    key = os.environ.get("API_KEY")
    if not key:
        raise ValueError("Error reaching Gemini: API_KEY environment variable is missing.")
    
    # Initialize the correct client from the new google-genai SDK
    client = genai.Client(api_key=key)
    return client

# Define the structured data schema
data_form = {
    "type": "OBJECT",
    "properties": {
        "name": {"type": "STRING"},
        "instructions_of_use": {"type": "STRING"},
        "warnings": {"type": "STRING"},
    },
    "required": ["name"] 
}

# NLP Prompt instructions
prompt = (
    "Extract name only. The name has no numbers or units. Then fill other data. "
    "If a value is not found, leave it as an empty string."
)

# Return image contents and classify with error handling
def perform_OCR(image_path, max_retries=5):
    client = client_creation()
    
    # Open image and scale it down to optimize token usage
    image = PIL.Image.open(image_path)
    
    # Pro-Tip: Gemini doesn't need 4K images for text extraction. 
    # Max size of 1024px preserves perfect text readability while slashing token overhead.
    image.thumbnail((1024, 1024))
    
    delay = 2  # Starting backoff delay in seconds
    
    for attempt in range(max_retries):
        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash-lite", 
                contents=[prompt, image],
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=data_form,
                ),
            )
            
            # Using the native SDK parser to return structured Python dict data
            return response.parsed
            
        except APIError as e:
            # Handle Quota Exceeded/Rate Limits (HTTP 429)
            if e.code == 429:
                print(f"Quota exceeded on attempt {attempt + 1}/{max_retries}. Retrying in {delay} seconds...")
                time.sleep(delay)
                delay *= 2  # Double the wait time for the next loop (2s, 4s, 8s, 16s...)
            else:
                # Re-raise any other severe API errors (like 400 bad request or 500 internal error)
                raise e
                
    raise RuntimeError(f"Failed to process {image_path} after {max_retries} attempts due to rate limits.")
