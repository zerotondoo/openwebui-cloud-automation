"""Main script for OpenWebUI automation."""

import logging
import webbrowser
import requests
from typing import Optional, Dict, Any
import tkinter as tk
from customtkinter import CTk, CTkButton, CTkLabel
from .webui_client import OpenWebUIClient
from .utils.config import Config
from .utils.error_handler import OpenWebUIError, AuthenticationError
from .utils.file_picker import FilePicker

class OpenWebUIAutomation:
    def __init__(self):
        """Initialize OpenWebUI automation."""
        self.config = Config()
        self.logger = logging.getLogger(__name__)
        self.client = OpenWebUIClient(self.config)
        self.file_picker = FilePicker()
        
        # Setup logging
        logging.basicConfig(**self.config.get_log_config())
        
    def check_auth(self) -> bool:
        """Check if we can authenticate with OpenWebUI."""
        try:
            models = self.client.list_models()
            if not models:
                self.logger.warning("Authentication required. Please set API key in config.yaml")
                return False
            return True
        except Exception as e:
            self.logger.error(f"Authentication Error: Failed to check authentication status - {e}")
            return False

    def _select_model(self) -> Optional[str]:
        """Select model from available models.
        
        Returns:
            Selected model name or None if cancelled
        """
        try:
            # For now, just return a hardcoded model
            return "meta-llama-3-8b-instruct"
            
        except Exception as e:
            self.logger.error(f"Model Selection Error: Failed to get available models - {e}")
            return None

    def run(self):
        """Run the automation workflow."""
        try:
            # Check authentication
            if not self.check_auth():
                return
                
            # Pick transcript file
            file_path = self.file_picker.pick_file()
            if not file_path:
                self.logger.info("File selection cancelled")
                return
                
            # Select model
            model = self._select_model()
            if not model:
                self.logger.info("Model selection cancelled")
                return
            
            # Create chat with file
            chat_response = self.client.create_chat(model, file_path)
            
            if chat_response["success"]:
                # If API call succeeded, open the chat URL with the model
                chat_url = f"{self.config.get_webui_url()}/?model={requests.utils.quote(model)}"
                
                # Display file ID prominently
                print("\n" + "="*50)
                print(f"📄 File uploaded successfully!")
                print(f"📎 File ID: {chat_response['file_id']}")
                print("\nTo use this file in your chat:")
                print("1. Wait for the chat window to open")
                print("2. Type # in the chat to see your uploaded files")
                print("3. Click on the file to reference it in your message")
                print("\nOr if you want to reference it manually:")
                print(f"#file-{chat_response['file_id']}")
                print("="*50 + "\n")
            else:
                # If API failed, just open new chat with model
                chat_url = f"{self.config.get_webui_url()}/?model={requests.utils.quote(model)}"
                self.logger.warning(f"Failed to create chat via API: {chat_response.get('error')}")
            
            self.logger.info(f"Opening chat URL: {chat_url}")
            webbrowser.open(chat_url)
            
            self.logger.info("Chat interface opened successfully")
            
        except OpenWebUIError as e:
            self.logger.error(f"OpenWebUI Error: {e}")
        except Exception as e:
            self.logger.error(f"Unexpected Error: An unexpected error occurred - {e}")

if __name__ == "__main__":
    automation = OpenWebUIAutomation()
    automation.run()
