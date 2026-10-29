
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

BACKEND_DIR = Path(__file__).resolve().parent.parent

class Settings(BaseSettings):
    app_name: str = "SupportIQ"
    jwt_secret: str = "replace-this-with-a-long-random-secret-before-use"
    access_token_minutes: int = 720
    database_url: str = "sqlite:///./supportiq.db"
    frontend_origin: str = "http://localhost:5173"

    gemini_api_key: str = ""
    gemini_model: str = "gemini-2.5-flash"

    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"
    chroma_path: str = "./chroma_data"
    max_upload_mb: int = 10

    model_config = SettingsConfigDict(
        env_file=BACKEND_DIR / ".env",
        extra="ignore",
        case_sensitive=False
    )

settings = Settings()
