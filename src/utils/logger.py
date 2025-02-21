"""Logging utility for OpenWebUI automation."""

import os
import logging
from logging.handlers import RotatingFileHandler
from typing import Dict, Any

class Logger:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Logger, cls).__new__(cls)
            cls._instance.logger = None
        return cls._instance

    def setup(self, config: Dict[str, Any]) -> None:
        """Setup logger with configuration.
        
        Args:
            config: Logging configuration from config.yaml
        """
        if self.logger is not None:
            return

        self.logger = logging.getLogger('OpenWebUIAutomation')
        self.logger.setLevel(getattr(logging, config['level']))

        # Create logs directory if it doesn't exist
        log_file = os.path.join(os.path.dirname(__file__), '../../logs/automation.log')
        os.makedirs(os.path.dirname(log_file), exist_ok=True)

        # Setup rotating file handler
        file_handler = RotatingFileHandler(
            log_file,
            maxBytes=config['max_size_mb'] * 1024 * 1024,
            backupCount=config['backup_count']
        )
        
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        file_handler.setFormatter(formatter)
        
        self.logger.addHandler(file_handler)

    def info(self, message: str) -> None:
        """Log info message."""
        if self.logger:
            self.logger.info(message)

    def error(self, message: str) -> None:
        """Log error message."""
        if self.logger:
            self.logger.error(message)

    def warning(self, message: str) -> None:
        """Log warning message."""
        if self.logger:
            self.logger.warning(message)

    def debug(self, message: str) -> None:
        """Log debug message."""
        if self.logger:
            self.logger.debug(message)
