from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str
    DB_DRIVER: str
    DATABASE_URL: str
    
    SMTP_HOST: str
    SMTP_PORT: int
    SMTP_USER: str
    SMTP_PASS: str
    
    REDIS_HOST: str
    REDIS_PORT: int
    
    SECRET_KEY: str
    HASH_ALGO: str
    
    model_config=SettingsConfigDict(env_file='.env')
    
    
settings = Settings()