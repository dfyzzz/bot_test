import logging
from datetime import datetime
from pathlib import Path


def setup_logger(name: str, log_file: str, level=logging.INFO):
    """Function to setup a logger with file and console handlers"""
    
    # Create logs directory if it doesn't exist
    Path(log_file).parent.mkdir(parents=True, exist_ok=True)
    
    # Create a custom logger
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Create handlers
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    console_handler = logging.StreamHandler()
    
    # Create formatters and add them to handlers
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    # Add handlers to the logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger


def log_user_action(user_id: int, action: str, details: str = ""):
    """Log user actions"""
    logger = setup_logger("user_actions", "logs/user_actions.log")
    logger.info(f"User {user_id}: {action} | Details: {details}")


def log_admin_action(admin_id: int, action: str, details: str = ""):
    """Log admin actions"""
    logger = setup_logger("admin_actions", "logs/admin_actions.log")
    logger.info(f"Admin {admin_id}: {action} | Details: {details}")


def log_system_event(event: str, details: str = ""):
    """Log system events"""
    logger = setup_logger("system_events", "logs/system_events.log")
    logger.info(f"System: {event} | Details: {details}")


def log_error(error: Exception, context: str = ""):
    """Log errors with context"""
    logger = setup_logger("errors", "logs/errors.log")
    logger.error(f"Error: {str(error)} | Context: {context}", exc_info=True)