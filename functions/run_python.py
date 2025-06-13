import os
import subprocess

def run_python_file(working_directory, file_path):
    try:
        original_file_path = file_path
        working_directory = os.path.abspath(working_directory)
        if not os.path.isabs(file_path):
            file_path = os.path.join(working_directory, file_path)
        file_path = os.path.abspath(file_path)

        if not file_path.startswith(working_directory):
             return f'Error: Cannot execute "{original_file_path}" as it is outside the permitted working directory'
        
        if not os.path.isfile(file_path):
            return f'Error: File "{original_file_path}" not found.'
        
        if not file_path.endswith(".py"):
            return f'Error: "{original_file_path}" is not a Python file.'
        
        result = subprocess.run(
             ["python3", file_path],
             capture_output=True,
             text=True,
             timeout=30,
             cwd=working_directory
             )
        
        final_output = []

        if result.stdout:
             final_output.append(f'STDOUT: {result.stdout}')

        if result.stderr:
             final_output.append(f'STDERR: {result.stderr}')

        if result.returncode != 0:
             final_output.append(f'Process exited with code {result.returncode}')

        if final_output:
            return "\n".join(final_output)
        else:
             return "No output produced"

    except Exception as e:
         return f"Error: executing Python file: {e}"