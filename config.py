import os
from dotenv import load_dotenv

load_dotenv()

CACHE_DIR = os.getenv("CACHE_DIR")
MODEL_NAME = os.getenv("MODEL_NAME")