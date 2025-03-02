from pathlib import Path
from typing import Dict

def load_config() -> Dict[str, str]:
    """Load configuration from .config file"""
    config = {}
    config_path = Path("configurations/.config")
    
    if not config_path.exists():
        raise FileNotFoundError("Configuration file not found")
    
    with open(config_path, "r") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#"):
                key, value = line.split("=", 1)
                config[key.strip()] = value.strip()
    
    return config

# Load configuration
try:
    config = load_config()
except Exception as e:
    raise Exception(f"Error loading configuration: {str(e)}")

# Configuration variables
SECRET_KEY = config.get("SECRET_KEY")
DATABASE_URL = config.get("DATABASE_URL")
ACCESS_TOKEN_EXPIRE_MINUTES = int(config.get("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
HOST = config.get("HOST", "127.0.0.1")
PORT = int(config.get("PORT", "8000"))
LOG_LEVEL = config.get("LOG_LEVEL", "INFO")
MAX_LOG_FILE_SIZE = int(config.get("MAX_LOG_FILE_SIZE", "1048576"))
LOG_BACKUP_COUNT = int(config.get("LOG_BACKUP_COUNT", "5")) 