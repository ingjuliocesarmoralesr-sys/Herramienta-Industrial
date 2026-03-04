from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "ViralTrendFinder API"
    database_url: str = "postgresql+psycopg2://postgres:postgres@localhost:5432/viraltrendfinder"
    youtube_api_key: str = ""
    reddit_user_agent: str = "ViralTrendFinder/1.0"
    allowed_origins: str = "http://localhost:3000"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
