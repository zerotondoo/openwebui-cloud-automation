"""Configuration manager for OpenWebUI automation."""

import os
import yaml
from typing import Dict, Any, Optional

class ConfigManager:
    def __init__(self, config_path: str = "../config.yaml"):
        """Initialize configuration manager.
        
        Args:
            config_path: Path to config.yaml file
        """
        self.config_path = os.path.join(os.path.dirname(__file__), config_path)
        self.config = self._load_config()

    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from yaml file."""
        try:
            with open(self.config_path, 'r') as f:
                return yaml.safe_load(f)
        except Exception as e:
            raise Exception(f"Failed to load config: {str(e)}")

    def save_config(self) -> None:
        """Save current configuration to yaml file."""
        try:
            with open(self.config_path, 'w') as f:
                yaml.dump(self.config, f, default_flow_style=False)
        except Exception as e:
            raise Exception(f"Failed to save config: {str(e)}")

    def get_transcript_folder(self) -> str:
        """Get configured transcript folder path."""
        return self.config['paths']['transcript_folder']

    def get_webui_url(self) -> str:
        """Get configured OpenWebUI URL."""
        return self.config['webui']['url']

    def get_api_key(self) -> Optional[str]:
        """Get API key if configured."""
        return self.config['webui'].get('api_key')

    def set_api_key(self, api_key: str) -> None:
        """Set API key in configuration."""
        self.config['webui']['api_key'] = api_key
        self.save_config()

    def get_default_model(self) -> str:
        """Get default model name."""
        return self.config['models']['default']

    def set_default_model(self, model: str) -> None:
        """Set default model in configuration."""
        self.config['models']['default'] = model
        self.save_config()

    def get_last_used_model(self) -> Optional[str]:
        """Get last used model name."""
        return self.config['models']['last_used']

    def set_last_used_model(self, model: str) -> None:
        """Set last used model in configuration."""
        self.config['models']['last_used'] = model
        self.save_config()

    def get_log_config(self) -> Dict[str, Any]:
        """Get logging configuration."""
        return self.config['logging']
