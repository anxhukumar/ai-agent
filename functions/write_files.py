import os

def write_file(working_directory, file_path, content):
    try:
        working_directory = os.path.abspath(working_directory)
        if not os.path.isabs(file_path):
                file_path = os.path.join(working_directory, file_path)
        file_path = os.path.abspath(file_path)

        if not file_path.startswith(working_directory):
             return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        try:
            dir_path = os.path.dirname(file_path)
            if not os.path.exists(dir_path):
                os.makedirs(dir_path)
        
        except Exception as e:
             return f'Error: Error while creating a file path'
        
        with open(file_path, "w") as f:
            f.write(content)
        
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
         return f"Error: Standard library - {e}"