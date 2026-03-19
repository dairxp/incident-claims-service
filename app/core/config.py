from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    APP_ENV: str = "development"
    APP_PORT: int = 8000
    API_KEY: str
    DATABASE_URL: str
    
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
