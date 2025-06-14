import os
import sys
from google import genai
from dotenv import load_dotenv
from functions.call_function import call_function

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

#Schema of get_file_content function
schema_get_file_content = genai.types.FunctionDeclaration(
    name="get_file_content",
    description="Gets the content of the specified file, that is constrained to the working directory.",
    parameters=genai.types.Schema(
        type=genai.types.Type.OBJECT,
        properties={
            "file_path": genai.types.Schema(
                type=genai.types.Type.STRING,
                description="The file path to get content from, relative to the working directory."
            )
        }
    )
)

#Schema of run_python_file function
schema_run_python_file = genai.types.FunctionDeclaration(
    name="run_python_file",
    description="Gets the output of the specified python file, that is constrained to the working directory.",
    parameters=genai.types.Schema(
        type=genai.types.Type.OBJECT,
        properties={
            "file_path": genai.types.Schema(
                type=genai.types.Type.STRING,
                description="The file path to get content from, relative to the working directory."
            )
        }
    )
)

#Schema of write_files function
schema_write_files = genai.types.FunctionDeclaration(
    name="write_files",
    description="Writes the provided content on a file if it exists at the provided location or creates a files if doesn't exist and it also creates any missing directories that are missing before the desired file path location.",
    parameters=genai.types.Schema(
        type=genai.types.Type.OBJECT,
        properties={
            "file_path": genai.types.Schema(
                type=genai.types.Type.STRING,
                description="The file path to get content from, relative to the working directory."
            ),
            "content": genai.types.Schema(
                type=genai.types.Type.STRING,
                description="The content that will be written to the file."
            )
        }
    )
)

available_functions = genai.types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_files

    ]
)

system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

response = client.models.generate_content(
    model='gemini-2.0-flash-001',
    contents=messages,
    config=genai.types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt)
)

function_call = response.function_calls

if not function_call:
    if "--verbose" in sys.argv:
        print(f"User prompt: {sys.argv[1]}\n Response: {response.text} Prompt tokens: {response.usage_metadata.prompt_token_count}\n Response tokens: {response.usage_metadata.candidates_token_count}")
    else:
        print(response.text)
    sys.exit(0)

try:
    function_output = call_function(function_call[0], verbose="--verbose" in sys.argv)
except Exception as e:
    print(f"Error calling function: {e}")
    sys.exit(1)

if function_output.parts[0].function_response.response:
    if "--verbose" in sys.argv:
        print(f"-> {function_output.parts[0].function_response.response}")
    else:
        print(function_output.parts[0].function_response.response["result"])