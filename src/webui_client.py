"""OpenWebUI API client for automation."""

import requests
import json
import os
from typing import Dict, List, Optional, Any
from .utils.error_handler import ConnectionError, AuthenticationError, ModelError, OpenWebUIError
import logging
from .utils.config import Config

class OpenWebUIClient:
    def __init__(self, config: Config):
        """Initialize WebUI client with configuration."""
        self.config = config
        self.logger = logging.getLogger(__name__)
        
        # Get API key from environment
        self.api_key = os.getenv('OPENWEBUI_API_KEY')
        if not self.api_key:
            raise ValueError("OPENWEBUI_API_KEY environment variable is required")
            
        # Common headers for all requests
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    def _make_request(self, method: str, endpoint: str, data: Optional[Dict] = None, files: Optional[Dict] = None, json: Optional[Dict] = None) -> Dict[str, Any]:
        """Make HTTP request to OpenWebUI API.
        
        Args:
            method: HTTP method (GET, POST, etc)
            endpoint: API endpoint
            data: Form data for POST/PUT
            files: Files to upload
            json: JSON data for POST/PUT
            
        Returns:
            Response data as dictionary
        """
        url = f"{self.config.get_webui_url()}{endpoint}"
        
        try:
            if method == 'GET':
                response = requests.get(url, headers=self.headers)
            elif method == 'POST':
                if files:
                    # For file uploads, don't include Content-Type header
                    headers = self.headers.copy()
                    headers.pop('Content-Type', None)
                    response = requests.post(url, headers=headers, data=data, files=files)
                elif json:
                    response = requests.post(url, headers=self.headers, json=json)
                else:
                    response = requests.post(url, headers=self.headers, json=data)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
                
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            self.logger.error(f"API request failed: {str(e)}")
            raise OpenWebUIError(f"API request failed: {str(e)}")
            
    def check_auth_required(self) -> bool:
        """Check if authentication is required.
        
        Returns:
            True if authentication is required, False otherwise
        """
        try:
            self._make_request('GET', '/api/models')  # Using correct OpenWebUI endpoint
            return False
        except AuthenticationError:
            return True
        except Exception:
            return True

    def list_models(self) -> List[Dict[str, Any]]:
        """List available models.
        
        Returns:
            List of model information dictionaries
        """
        try:
            response = self._make_request('GET', '/api/models')  # Using correct OpenWebUI endpoint
            if not response or not isinstance(response, dict):
                raise OpenWebUIError("Invalid response format")
                
            return response.get('data', [])
            
        except Exception as e:
            self.logger.error(f"Failed to list models: {str(e)}")
            return []
            
    def upload_document(self, file_path: str) -> Dict[str, Any]:
        """Upload a document to OpenWebUI's document storage.
        
        Args:
            file_path: Path to the file to upload
            
        Returns:
            Response from the upload API
        """
        self.logger.info(f"Uploading document: {file_path}")
        
        try:
            # Upload file
            file_name = os.path.basename(file_path)
            files = {
                'file': (file_name, open(file_path, 'rb'), 'text/plain')
            }
            headers = self.headers.copy()
            headers.pop('Content-Type', None)  # Let requests set the correct content type for multipart
            headers['Accept'] = 'application/json'
            
            # Upload the file using OpenWebUI endpoint
            upload_url = f"{self.config.get_webui_url()}/api/files/"
            upload_response = requests.post(
                upload_url,
                headers=headers,
                files=files
            )
            
            self.logger.debug(f"Upload response: {upload_response.text}")
            
            if upload_response.status_code != 200:
                raise OpenWebUIError(f"Upload failed: {upload_response.text}")
                
            # Get file ID from response
            file_id = upload_response.json().get('id')
            if not file_id:
                raise OpenWebUIError("No file ID in response")
                
            self.logger.info("Document uploaded successfully")
            return {
                "success": True,
                "file_id": file_id,
                "response": upload_response.json()
            }
            
        except Exception as e:
            self.logger.error(f"Failed to upload document: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
            
    def create_chat(
        self,
        model: str,
        file_path: str
    ) -> Dict[str, Any]:
        """Create new chat with file reference.
        
        Args:
            model: Model to use for chat
            file_path: Path to transcript file
            
        Returns:
            Chat session information
        """
        try:
            # First upload the document
            upload_result = self.upload_document(file_path)
            if not upload_result["success"]:
                return upload_result
                
            # Create a new chat using OpenWebUI endpoint
            chat_data = {
                "model": model,
                "messages": [],  # Empty initial messages
                "file_ids": [upload_result["file_id"]]
            }
            
            chat_response = self._make_request('POST', '/api/chat/completions', json=chat_data)
            
            return {
                "success": True,
                "file_id": upload_result["file_id"],
                "chat_id": chat_response.get("id"),
                "response": chat_response
            }
            
        except Exception as e:
            self.logger.error(f"Failed to create chat: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
