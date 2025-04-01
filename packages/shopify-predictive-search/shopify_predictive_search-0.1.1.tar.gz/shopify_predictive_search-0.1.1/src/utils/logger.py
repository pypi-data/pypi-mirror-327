# src/shopify_search/utils/logger.py
import logging
import sys
import os
from logging.handlers import RotatingFileHandler
from src.config import Config

def setup_logger():
    config = Config()
    logger = logging.getLogger('ShopifySearch')
    logger.setLevel(config.LOG_LEVEL)
    
    # Create logs directory if it doesn't exist
    os.makedirs('logs', exist_ok=True)
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    ))
    
    # File handler
    file_handler = RotatingFileHandler(
        'logs/shopify_search.log',
        maxBytes=1024 * 1024,  # 1MB
        backupCount=5
    )
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    ))
    
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    
    return logger