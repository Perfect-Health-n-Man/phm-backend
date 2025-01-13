from dotenv import load_dotenv
load_dotenv()

import os
from pathlib import Path

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

LANGFUSE_HOST = os.getenv('LANGFUSE_HOST')
LANGFUSE_PUBLIC_KEY = os.getenv('LANGFUSE_PUBLIC_KEY')
LANGFUSE_SECRET_KEY = os.getenv('LANGFUSE_SECRET_KEY')

BASE_DIR = Path(__file__).resolve().parent
# print(BASE_DIR)
credentials_path = os.path.join(BASE_DIR, 'sa_keyfile.json')
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credentials_path
