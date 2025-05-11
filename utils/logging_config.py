import logging
from logging.handlers import RotatingFileHandler
import os

def setup_logging():
    # Set up a rotating file handler for logs
    log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logs')
    os.makedirs(log_dir, exist_ok=True)

    log_path = os.path.join(log_dir, 'app.log')
    file_handler = RotatingFileHandler(log_path, maxBytes=5*1024*1024, backupCount=3)
    file_handler.setLevel(logging.DEBUG)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.WARNING)

    log_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    file_handler.setFormatter(log_formatter)
    console_handler.setFormatter(log_formatter)

    # Get root logger and set its level
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logger.handlers = []  # Clear existing handlers
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    # Silence noisy libraries
    logging.getLogger("pymongo").setLevel(logging.WARNING)
