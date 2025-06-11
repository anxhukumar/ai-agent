import os
from dotenv import load_dotenv
from google import genai
import sys

load_dotenv()

if len(sys.argv) != 2:
    print('Correct usage: python3 main.py < "prompt" >')
    sys.exit(1)

api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

response = client.models.generate_content(
    model='gemini-2.0-flash-001', contents=f'{sys.argv[1]}'
)
print(f"Response: {response.text} Prompt tokens: {response.usage_metadata.prompt_token_count} Response tokens: {response.usage_metadata.candidates_token_count}")