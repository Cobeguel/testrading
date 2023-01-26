import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))


def generate_path(relative: str) -> str:
    return os.path.join(ROOT_DIR, relative)


DB_CONFIG_FILE = generate_path('config/database.yml')
