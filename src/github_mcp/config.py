from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

PROJECT_ROOT = Path(__file__).resolve().parents[2]

class Settings(BaseSettings):
    github_token: str
    github_api_base: str = "https://api.github.com"
    request_timeout: float = 15.0

    model_config = SettingsConfigDict(
        env_file= PROJECT_ROOT / ".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()