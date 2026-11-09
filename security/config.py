from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    SECRET_KEY: str = "development-only-change-me"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRES_MINUTES: int = 30
    DATABASE_URL: str = "sqlite:///data.db"

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()