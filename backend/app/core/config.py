from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    openai_api_key: str
    environment: str = "development"
    fastapi_host: str = "0.0.0.0"
    fastapi_port: int = 8000
    db_path: str = "../data/feedbacks.db"
    chroma_path: str = "../data/chroma"
    max_feedbacks_per_upload: int = 10000
    llm_timeout_seconds: int = 30

    class Config:
        env_file = ".env"


settings = Settings()