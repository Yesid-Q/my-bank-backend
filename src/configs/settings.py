import ssl

from typing import List
from pydantic import BaseSettings

class Settings(BaseSettings):
    DEBUG: bool
    APP_NAME: str
    DESCRIPTION: str
    VERSION: str
    SECRET_KEY: str

    DATABASE_URL: str
    DATABASE_DRIVER: str
    DATABASE_USER: str
    DATABASE_PASSWORD: str
    DATABASE_PORT: int
    DATABASE_DATABASE: str

    TOKEN_ALGORITHM: str

    MODELS: List[str] = [
        'src.models.account_model',
        'src.models.document_model',
        'src.models.type_account_model',
        'src.models.user_model',
        'src.models.transaction_model'
    ]

    class Config:
        env_file_encoding = 'utf-8'

settings = Settings()

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

TORTOISE_ORM = {
    'connections': {
        'default': {
            'engine': 'tortoise.backends.asyncpg',
            'credentials': {
                'database': settings.DATABASE_DATABASE,
                'host': settings.DATABASE_URL,
                'password': settings.DATABASE_PASSWORD,
                'port': settings.DATABASE_PORT,
                'user': settings.DATABASE_USER,
                'ssl': 'disable' if settings.DEBUG else ctx
            }
        }
    },
    'apps': {
        'models': {
            'models': settings.MODELS,
            'default_connection': 'default',
        }
    },
    'use_tz': False,
    'timezone': 'UTC'
}