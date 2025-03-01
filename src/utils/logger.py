import logging
import os
from datetime import datetime
from logging.handlers import RotatingFileHandler

# Create logs directory if it doesn't exist
logs_dir = "logs"
if not os.path.exists(logs_dir):
    os.makedirs(logs_dir)

# Configure logging
logger = logging.getLogger("post_management_api")
logger.setLevel(logging.INFO)

# Create handlers
file_handler = RotatingFileHandler(
    filename=f"logs/app_{datetime.now().strftime('%Y%m%d')}.log",
    maxBytes=1024 * 1024,  # 1MB
    backupCount=5
)
console_handler = logging.StreamHandler()

# Create formatters and add it to handlers
log_format = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
file_handler.setFormatter(log_format)
console_handler.setFormatter(log_format)

# Add handlers to the logger
logger.addHandler(file_handler)
logger.addHandler(console_handler) 