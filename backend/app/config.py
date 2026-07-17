from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    SUPABASE_URL: str
    SUPABASE_JWT_SECRET: str
    DATABASE_URL: str
    GROQ_API_KEY: str
    CORS_ORIGINS: str = "http://localhost:3000"
    UPLOAD_DIR: str = "./uploads"

    class Config:
        env_file = ".env"

    @property
    def cors_origin_list(self):
        return [o.strip() for o in self.CORS_ORIGINS.split(",")]


@lru_cache
def get_settings() -> Settings:
    return Settings()
