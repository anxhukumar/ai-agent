import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

response = client.models.generate_content(
    model='gemini-2.0-flash-001', contents='Why is the sky blue? Answer in one line.'
)
print(f"Response: {response.text} Prompt tokens: {response.usage_metadata.prompt_token_count} Response tokens: {response.usage_metadata.candidates_token_count}")