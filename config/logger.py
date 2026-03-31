"""
Logging configuration for AI Database Agent
Provides centralized logging to both file and console
"""

import logging
import os
from datetime import datetime


def setup_logger(name, log_level=logging.INFO):
    """
    Setup logging for all modules
    
    Args:
        name: Logger name (typically __name__)
        log_level: Logging level (INFO, DEBUG, WARNING, ERROR)
    
    Returns:
        Configured logger instance
    """
    
    # Create logs directory if it doesn't exist
    log_dir = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "logs"
    )
    os.makedirs(log_dir, exist_ok=True)
    
    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    # Prevent duplicate handlers
    if logger.hasHandlers():
        return logger
    
    # File handler - logs everything to file
    log_file = os.path.join(
        log_dir,
        f"ai_agent_{datetime.now().strftime('%Y%m%d')}.log"
    )
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.DEBUG)
    
    # Console handler - logs INFO and above to console
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    
    # Formatter
    detailed_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    console_formatter = logging.Formatter(
        '%(levelname)s - %(message)s'
    )
    
    file_handler.setFormatter(detailed_formatter)
    console_handler.setFormatter(console_formatter)
    
    # Add handlers to logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger


# Initialize root logger for the project
root_logger = setup_logger("ai_db_agent")
