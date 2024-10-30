import pathlib
from dotenv import load_dotenv
import os

def path_exists(path):
    return os.path.exists(path)


def folder_exits(folder_path):
    return os.path.isdir(folder_path)


def file_exists(file_path):
    return os.path.isfile(file_path)

def get_file_path(relative_file_path=''):
    return str(os.path.join(pathlib.Path(__file__).absolute().parent.parent.parent, relative_file_path))


if file_exists('/config/.env'):
    env_file = '/config/.env'
else:
    env_file = get_file_path(".env")

load_dotenv(env_file)


def get(env_key, default_value=None):
    return os.getenv(env_key, default_value)