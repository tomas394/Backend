from typing import List, Union
from pydantic import AnyHttpUrl, validator
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = "Guardi.IA"
    API_V1_STR: str = "/api/v1"

    # DATABASE
    # If running in Docker, host might be "db". If running locally with Docker exposed ports, "localhost".
    # We default to localhost for development outside the container connecting to the container.
    POSTGRES_SERVER: str = "localhost"
    POSTGRES_USER: str = "guardi_user"
    POSTGRES_PASSWORD: str = "guardi_password"
    POSTGRES_DB: str = "guardi_db"
    POSTGRES_PORT: int = 5432
    DATABASE_URI: Union[str, None] = None

    @validator("DATABASE_URI", pre=True)
    def assemble_db_connection(cls, v: Union[str, None], values: dict[str, any]) -> str:
        if isinstance(v, str):
            return v
        return f"postgresql+asyncpg://{values.get('POSTGRES_USER')}:{values.get('POSTGRES_PASSWORD')}@{values.get('POSTGRES_SERVER')}:{values.get('POSTGRES_PORT')}/{values.get('POSTGRES_DB')}"

    # SECURITY
    SECRET_KEY: str = "CHANGEME_SUPER_SECRET_KEY_FOR_JWT_SIGNING" # In prod, get from env
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # IOT / WEBHOOKS
    TERRA_WEBHOOK_SECRET: str = "CHANGEME_TERRA_SECRET" # Shared secret for HMAC

    # CORS
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    model_config = SettingsConfigDict(case_sensitive=True, env_file=".env")

settings = Settings()
