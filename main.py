import os
from dotenv import load_dotenv
from google import genai
import sys

load_dotenv()

if len(sys.argv) < 2:
    print('Correct usage: python3 main.py <prompt> [--verbose]')
    sys.exit(1)

api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

messages = [
    genai.types.Content(role="user", parts=[genai.types.Part(text=sys.argv[1])]),
    ]

response = client.models.generate_content(
    model='gemini-2.0-flash-001', contents=f'{messages}'
)

if "--verbose" in sys.argv:
    print(f"User prompt: {sys.argv[1]}\n Response: {response.text} Prompt tokens: {response.usage_metadata.prompt_token_count}\n Response tokens: {response.usage_metadata.candidates_token_count}")
else:
    print(response.text)