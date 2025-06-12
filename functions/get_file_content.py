import os

def get_file_content(working_directory, file_path):
    try:
        working_directory = os.path.abspath(working_directory)
        if not os.path.isabs(file_path):
                file_path = os.path.join(working_directory, file_path)
        file_path = os.path.abspath(file_path)

        if not file_path.startswith(working_directory):
             return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        
        if not os.path.isfile(file_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        
        MAX_CHARS = 10000
        
        with open(file_path, "r") as f:
             file_content_string = f.read(MAX_CHARS)
             if len(f.read(1)) >= 1:
                  file_content_string += f'...File "{file_path}" truncated at 10000 characters'
        return file_content_string
    
    except Exception as e:
        return f"Error: Standard library - {e}"