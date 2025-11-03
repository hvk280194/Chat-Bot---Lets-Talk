import os
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseModel):
    APP_NAME: str = "nebula-chat-service"
    ENV: str = os.getenv("ENV", "dev")

    PROVIDER: str = os.getenv("PROVIDER", "hfhub")  # "hfhub" or "ollama"
    OLLAMA_MODEL: str = os.getenv("OLLAMA_MODEL", "mistral")
    OLLAMA_BASE_URL: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")

    HFHUB_REPO_ID: str = os.getenv("HFHUB_REPO_ID", "mistralai/Mistral-7B-Instruct-v0.2")
    HFHUB_API_TOKEN: str = os.getenv("HFHUB_API_TOKEN", "")

    MAX_TOKENS: int = int(os.getenv("MAX_TOKENS", "512"))
    SSE_CHUNK_DELAY_MS: int = int(os.getenv("SSE_CHUNK_DELAY_MS", "0"))

settings = Settings()
print("✅ HF TOKEN PREFIX:", settings.HFHUB_API_TOKEN[:10] if settings.HFHUB_API_TOKEN else "None found")

