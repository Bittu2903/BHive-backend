import pathlib
import os
from dotenv import load_dotenv

def path_exists(path):
    """Check if a given path exists.

    Args:
        path (str): The path to check.

    Returns:
        bool: True if the path exists, otherwise False.
    """
    return os.path.exists(path)

def folder_exists(folder_path):
    """Check if a given folder exists.

    Args:
        folder_path (str): The folder path to check.

    Returns:
        bool: True if the folder exists, otherwise False.
    """
    return os.path.isdir(folder_path)

def file_exists(file_path):
    """Check if a given file exists.

    Args:
        file_path (str): The file path to check.

    Returns:
        bool: True if the file exists, otherwise False.
    """
    return os.path.isfile(file_path)

def get_file_path(relative_file_path=''):
    """Get the absolute file path based on the given relative path.

    Args:
        relative_file_path (str): The relative file path.

    Returns:
        str: The absolute file path.
    """
    return str(os.path.join(pathlib.Path(__file__).absolute().parent.parent.parent, relative_file_path))

# Load the .env file from the specified location
if file_exists('/config/.env'):
    env_file = '/config/.env'
else:
    env_file = get_file_path(".env")

load_dotenv(env_file)

def get(env_key, default_value=None):
    """Retrieve an environment variable value.

    Args:
        env_key (str): The key of the environment variable.
        default_value: The default value to return if the variable is not found.

    Returns:
        str: The value of the environment variable, or the default value if not found.
    """
    return os.getenv(env_key, default_value)
