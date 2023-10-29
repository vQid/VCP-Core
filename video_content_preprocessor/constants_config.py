import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(dotenv_path=".env")

# Load environment Variables
DOWNLOAD_ROOT_DIRECTORY = Path(os.getenv("DOWNLOAD_ROOT_DIRECTORY"))
DEVELOPER_KEY = os.environ.get('DEVELOPER_KEY')
MAIN_PATH = Path(os.environ.get('MAIN_PATH'))
