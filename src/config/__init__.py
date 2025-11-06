"""Configuration module for DigiLib Assistant."""

import os
from dotenv import load_dotenv

# Load environment variables from .env file (if exists, for local development)
# Railway/production uses environment variables directly
load_dotenv(override=False)

# Telegram Bot Configuration
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")

# Yandex GPT Configuration
YANDEX_GPT_API_KEY = os.getenv("YANDEX_GPT_API_KEY", "")
YANDEX_FOLDER_ID = os.getenv("YANDEX_FOLDER_ID", "")

# Database Configuration
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./digilib.db")

# Application Settings
DEBUG = os.getenv("DEBUG", "True").lower() == "true"
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# Rate Limiting
GPT_REQUESTS_PER_HOUR = int(os.getenv("GPT_REQUESTS_PER_HOUR", "10"))
GPT_REQUESTS_PER_DAY = int(os.getenv("GPT_REQUESTS_PER_DAY", "50"))


def validate_config() -> bool:
    """Validate that all required configuration is present."""
    if not TELEGRAM_BOT_TOKEN:
        print("❌ ERROR: TELEGRAM_BOT_TOKEN is not set")
        print("   Please check:")
        print("   - Railway: Variables tab")
        print("   - Local: .env file")
        print(f"   Current value: '{TELEGRAM_BOT_TOKEN}'")
        return False
    
    print("✅ Configuration loaded successfully")
    print(f"   - Debug Mode: {DEBUG}")
    print(f"   - Log Level: {LOG_LEVEL}")
    print(f"   - Bot Token: {'*' * 20}{TELEGRAM_BOT_TOKEN[-4:]}")
    
    # Log Yandex GPT status
    if YANDEX_GPT_API_KEY and YANDEX_FOLDER_ID:
        print(f"   - Yandex GPT: Configured ✅")
    else:
        print(f"   - Yandex GPT: Not configured (Creative Mode will show instructions)")
    
    return True
