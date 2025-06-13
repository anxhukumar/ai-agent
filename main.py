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

#Schema of get_files_info function
schema_get_files_info = genai.types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=genai.types.Schema(
        type=genai.types.Type.OBJECT,
        properties={
            "directory": genai.types.Schema(
                type=genai.types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)

available_functions = genai.types.Tool(
    function_declarations=[
        schema_get_files_info,
    ]
)

system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

response = client.models.generate_content(
    model='gemini-2.0-flash-001',
    contents=messages,
    config=genai.types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt)
)

function_call = response.function_calls

if function_call:
    print(f"Calling function: {function_call[0].name}({function_call[0].args})")
else:
    if "--verbose" in sys.argv:
        print(f"User prompt: {sys.argv[1]}\n Response: {response.text} Prompt tokens: {response.usage_metadata.prompt_token_count}\n Response tokens: {response.usage_metadata.candidates_token_count}")
    else:
        print(response.text)