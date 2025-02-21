#!/usr/bin/env python3
"""Entry point for OpenWebUI automation."""

import os
import sys
from dotenv import load_dotenv

# Add src directory to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

# Load environment variables from .env file
load_dotenv()

from src.main import OpenWebUIAutomation

if __name__ == "__main__":
    app = OpenWebUIAutomation()
    app.run()
