from pydantic import BaseSettings


class Settings(BaseSettings):
    # Database
    database_url: str

    # AWS
    aws_region: str = "us-west-2"

    # Other configs (e.g., API keys) can go here later

    class Config:
        env_file = ".env"  # Load from .env automatically


# Singleton settings object
settings = Settings()

