import os
from dotenv import load_dotenv

load_dotenv()

class Settings():
    RENDER_API_URL: str
    RENDER_API_TOKEN: str
    AUTH_SERVICE_URL: str


    def __init__(self):
        self.RENDER_API_URL = os.getenv("RENDER_API_URL")
        self.RENDER_API_TOKEN = os.getenv("RENDER_API_TOKEN")
        self.AUTH_SERVICE_URL = os.getenv("AUTH_SERVICE_URL")

settings = Settings()