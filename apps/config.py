from pydantic_settings import BaseSettings

# This is added to check if all the necessary env vars are present 

class Settings(BaseSettings):
    DB_HOST: str 
    DB_PORT: str
    DB_PASS: str 
    DB_USER: str 
    SECRET_KEY: str 

setting = Settings()