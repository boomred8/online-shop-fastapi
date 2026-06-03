import os
from dotenv import load_dotenv


load_dotenv()


DATABASE = os.getenv("PG_DATABASE")
SECRET_KEY = os.getenv("SECRET_KEY")


if not DATABASE:
    raise Exception("PG_DATABASE environment variable is not set")


if not SECRET_KEY:
    raise Exception("SECRET_KEY environment variable is not set")