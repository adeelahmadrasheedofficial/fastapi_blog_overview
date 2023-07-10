from pydantic import BaseSettings


# Setting up environment variables with pydantic BaseSettings
class Settings(BaseSettings):
    database_hostname: str
    database_name: str
    database_port: str
    database_username: str
    database_password: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    class Config:
        env_file = ".env"


settings = Settings()
