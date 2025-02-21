"""File picker dialog for transcript files."""

import os
import tkinter as tk
from tkinter import filedialog
from typing import Optional
import logging

class FilePicker:
    """File picker dialog for selecting transcript files."""
    
    def __init__(self):
        """Initialize file picker."""
        self.logger = logging.getLogger(__name__)
        
    def pick_file(self) -> Optional[str]:
        """Show file picker dialog.
        
        Returns:
            Selected file path or None if cancelled
        """
        try:
            root = tk.Tk()
            root.withdraw()  # Hide the main window
            
            file_path = filedialog.askopenfilename(
                title="Select Transcript File",
                filetypes=[
                    ("Text Files", "*.txt"),
                    ("All Files", "*.*")
                ]
            )
            
            if not file_path:
                self.logger.info("File selection cancelled")
                return None
                
            self.logger.info(f"Selected file: {file_path}")
            return file_path
            
        except Exception as e:
            self.logger.error(f"Error picking file: {str(e)}")
            return None
            
    def read_file_content(self, file_path: str) -> Optional[str]:
        """Read content from selected file.
        
        Args:
            file_path: Path to file to read
            
        Returns:
            File content as string or None if error
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            self.logger.info(f"Read {len(content)} characters from file")
            return content
            
        except Exception as e:
            self.logger.error(f"Error reading file: {str(e)}")
            return None
