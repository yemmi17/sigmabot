from dataclasses import dataclass
import os
from dotenv import load_dotenv

load_dotenv()


@dataclass
class Settings:
    BOT_TOKEN: str = os.getenv("BOT_TOKEN", "")
    WEBHOOK_HOST: str = os.getenv("WEBHOOK_HOST", "")
    WEBHOOK_PATH: str = os.getenv("WEBHOOK_PATH", "/webhook")
    WEBHOOK_URL: str = os.getenv("WEBHOOK_URL", "")
    WEBAPP_HOST: str = os.getenv("WEBAPP_HOST", "0.0.0.0")
    WEBAPP_PORT: int = int(os.getenv("WEBAPP_PORT", "8000"))


settings = Settings()
