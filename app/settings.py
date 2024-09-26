""" Application Settings Module
"""
import os
from dotenv import load_dotenv

load_dotenv()

def get_connection_string(asyncMode: bool = False, testMode: bool = False) -> str:
    engine = os.environ.get("DB_ENGINE") if not asyncMode else os.environ.get("ASYNC_DB_ENGINE")
    dbhost = os.environ.get("DB_HOST")
    username = os.environ.get("DB_USERNAME")
    password = os.environ.get("DB_PASSWORD")
    dbname = os.environ.get("DB_NAME") if not testMode else os.environ.get("TEST_DB_NAME")
    return f"{engine}://{username}:{password}@{dbhost}/{dbname}"

# Database Setting
SQLALCHEMY_DATABASE_URL = get_connection_string()
SQLALCHEMY_DATABASE_URL_ASYNC = get_connection_string(asyncMode=True)
SQLALCHEMY_DATABASE_URL_TEST = get_connection_string(testMode=True)

# # JWT Setting
JWT_SECRET = os.environ.get("JWT_SECRET")
JWT_ALGORITHM = os.environ.get("JWT_ALGORITHM")