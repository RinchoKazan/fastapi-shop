from typing import List
from pydantic_settings import BaseSettings

"""
класс settings 
app_name название приложения
debug позволяет видеть ошибки во время разрабботки на продакшене выключают
database_url путь
"""

class Settings(BaseSettings):
    app_name: str = "FastAPI Shop"
    debug: bool = True
    database_url: str = "sqlite:/// ./shop.db"
    cors_origins: List[str] = [
        "http://localhost:5173",
        "http://localhost:3000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000",
    ]
    static_dir: str = "static"
    images_dir: str = "static/images"

    class Config:
        env_file = ".env"

settings = Settings()