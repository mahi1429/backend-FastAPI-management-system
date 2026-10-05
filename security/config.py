from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings():
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRES_MINUTES: int = 30

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()
