import os


class Settings:
    """Minimal settings loaded from environment variables."""

    def __init__(self):
        self.database_url: str = os.getenv("DATABASE_URL", "sqlite:///./app.db")
        self.aws_region: str = os.getenv("AWS_REGION", "us-west-2")


# Singleton settings object
settings = Settings()
