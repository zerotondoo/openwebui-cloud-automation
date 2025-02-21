#!/usr/bin/env python3
import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
BASE_URL = "http://10.130.141.101:3000"
TEST_MODEL = "meta-llama-3-8b-instruct"  # One of the models we saw in the list
TEST_MESSAGE = "Hello, this is a test message"  # Short test message to start with

# Get API key from environment or ask user
API_KEY = os.getenv('OPENWEBUI_API_KEY')
if not API_KEY:
    print("Please enter your OpenWebUI API key (find it in Settings > Account):")
    API_KEY = input().strip()

# Common headers
HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

def test_create_chat():
    """Test creating a new chat session"""
    url = f"{BASE_URL}/api/chat/completions"
    
    # Basic payload following OpenAI format
    payload = {
        "model": TEST_MODEL,
        "messages": [
            {
                "role": "user",
                "content": TEST_MESSAGE
            }
        ],
        "stream": False  # Important: disable streaming for testing
    }
    
    print(f"\nTrying to create chat with payload:\n{json.dumps(payload, indent=2)}")
    
    try:
        response = requests.post(url, json=payload, headers=HEADERS)
        print(f"\nStatus Code: {response.status_code}")
        print(f"Response:\n{json.dumps(response.json(), indent=2)}")
    except Exception as e:
        print(f"Error: {str(e)}")

def test_list_models():
    """Test listing available models"""
    url = f"{BASE_URL}/api/models"
    
    try:
        response = requests.get(url, headers=HEADERS)
        print(f"\nStatus Code: {response.status_code}")
        print(f"Models:\n{json.dumps(response.json(), indent=2)}")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    if not API_KEY:
        print("Error: No API key provided")
        exit(1)
        
    print("=== Testing OpenWebUI API ===")
    print(f"Using API key: {API_KEY[:8]}...")  # Only show first 8 chars for security
    test_list_models()
    test_create_chat()
