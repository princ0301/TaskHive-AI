from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    GROQ_API_KEY: str = ""
    GROQ_MODEL: str = "meta-llama/llama-4-scout-17b-16e-instruct"

    SERPER_API_KEY: str = ""

    DATABASE_URL: str = "sqlite:///./multi_agent.db"

    REDIS_URL: str = "redis://localhost:6379/0"

    CHROMA_DB_PATH: str = "./chroma_db"

    class Config:
        env_file = ".env"

settings = Settings()