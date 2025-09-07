from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    SERPAPI_KEY: str | None = None
    BING_API_KEY: str | None = None
    OPENAI_API_KEY: str | None = None

    model_config = SettingsConfigDict(env_file=".env")
    

settings = Settings()
