from dotenv import load_dotenv
load_dotenv()

import os

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

LANGFUSE_HOST = os.getenv('LANGFUSE_HOST')
LANGFUSE_PUBLIC_KEY = os.getenv('LANGFUSE_PUBLIC_KEY')
LANGFUSE_SECRET_KEY = os.getenv('LANGFUSE_SECRET_KEY')