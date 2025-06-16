# backend/app/config.py

from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv  # <-- 1. IMPORT load_dotenv
import os # <-- IMPORT os to construct the path

# 2. CONSTRUCT PATH AND LOAD THE .env FILE EXPLICITLY
# This creates a path to the .env file located in the parent directory (backend/)
dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(dotenv_path=dotenv_path)


class Settings(BaseSettings):
    # This will now read from the environment variables loaded by load_dotenv()
    database_url: str

    # We no longer need the env_file setting here as we are loading it manually

    # JWT Authentication settings
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int


# Create a single, reusable instance of the Settings class
settings = Settings()