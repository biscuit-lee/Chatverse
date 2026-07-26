
from dotenv import load_dotenv
import os

load_dotenv()
class Settings:
    GRPQ_API_KEY = os.getenv("GRPQ_API_KEY")


settings = Settings()