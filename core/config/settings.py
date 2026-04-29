import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    ENVIRONMENT = os.getenv("ENVIRONMENT", "test")

    BASE_URLS = {
        "test": os.getenv("TEST_BASE_URL"),
        "prod": os.getenv("PROD_BASE_URL"),
    }

    @classmethod
    def get_base_url(cls):
        return cls.BASE_URLS.get(cls.ENVIRONMENT)