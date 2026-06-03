import os
from dotenv import load_dotenv

load_dotenv()

DATABASE = os.getenv('PG_DATABASE')
secret_key = os.getenv('SESSION_SECRET_KEY')

if not DATABASE:
    raise Exception('DATABASE environment variable is not set')
if not secret_key:
    raise Exception('SECRET_KEY environment variable is not set')


