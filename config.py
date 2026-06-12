from dotenv import load_dotenv
import os

load_dotenv()

APP_NAME = os.getenv("APP_NAME")
APP_VERSION = os.getenv("APP_VERSION")

USAJOBS_EMAIL = os.getenv("USAJOBS_EMAIL")
USAJOBS_API_KEY = os.getenv("USAJOBS_API_KEY")

JOOBLE_API_KEY = os.getenv(
    "JOOBLE_API_KEY"
)

ADZUNA_APP_ID = os.getenv(
    "ADZUNA_APP_ID"
)

ADZUNA_APP_KEY = os.getenv(
    "ADZUNA_APP_KEY"
)