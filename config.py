from dotenv import load_dotenv
load_dotenv()

import os

LANGFUSE_HOST = os.getenv('LANGFUSE_HOST')
LANGFUSE_PUBLIC_KEY = os.getenv('LANGFUSE_PUBLIC_KEY')
LANGFUSE_SECRET_KEY = os.getenv('LANGFUSE_SECRET_KEY')