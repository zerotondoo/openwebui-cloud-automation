"""Configuration management for OpenWebUI automation."""

import os
import yaml
import logging
from typing import Optional, Dict, Any

class Config:
    """Configuration manager."""
    
    def __init__(self):
        """Initialize configuration."""
        self.config = self._load_config()
        self.webui_url = self.config['webui']['url']
        
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from yaml file."""
        config_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'config.yaml')
        with open(config_path, 'r') as f:
            return yaml.safe_load(f)
        
    def get_webui_url(self) -> str:
        """Get OpenWebUI base URL."""
        return self.webui_url.rstrip('/')
        
    def get_log_config(self) -> Dict[str, Any]:
        """Get logging configuration."""
        return {
            'level': logging.INFO,
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S'
        }
