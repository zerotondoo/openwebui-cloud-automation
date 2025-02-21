"""Configuration management for OpenWebUI automation."""

import os
import logging
from typing import Optional, Dict, Any

class Config:
    """Configuration manager."""
    
    def __init__(self):
        """Initialize configuration."""
        self.webui_url = os.getenv('OPENWEBUI_URL', 'http://10.130.141.101:3000')
        
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
