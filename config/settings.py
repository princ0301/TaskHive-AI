from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    LLM_PROVIDER: str = "groq"  # Options: "groq", "ollama", "openrouter"
     
    GROQ_API_KEY: str = ""
    GROQ_MODEL: str = "meta-llama/llama-4-scout-17b-16e-instruct"
     
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    OLLAMA_MODEL: str = "gpt-oss-120b"
    OLLAMA_API_KEY: str = ""
     
    SERPER_API_KEY: str = ""
 
    DATABASE_URL: str = "sqlite:///./multi_agent.db"
    REDIS_URL: str = "redis://localhost:6379/0"
    CHROMA_DB_PATH: str = "./chroma_db"

    class Config:
        env_file = ".env"

settings = Settings()
