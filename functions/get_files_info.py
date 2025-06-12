import os

def get_files_info(working_directory, directory=None):
    try:
        working_directory = os.path.abspath(working_directory)
        
        if directory is None:
            directory = working_directory
        else:
            if not os.path.isabs(directory):
                directory = os.path.join(working_directory, directory)
            directory = os.path.abspath(directory)

        if not directory.startswith(working_directory):
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        if not os.path.isdir(directory):
            return f'Error: "{directory}" is not a directory'
        
        dir_info = []
        
        for content in os.listdir(directory):
            is_dir = os.path.isdir(os.path.join(directory, content))
            size = os.path.getsize(os.path.join(directory, content))
            dir_info.append(f"- {content}: file_size={size} bytes, is_dir={is_dir}")
        return "\n".join(dir_info)
    except Exception as e:
        return f"Error: Standard library - {e}"
