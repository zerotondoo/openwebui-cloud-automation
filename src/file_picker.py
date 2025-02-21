"""File picker utility for OpenWebUI automation."""

import os
import tkinter as tk
from tkinter import filedialog
from typing import Optional
from src.utils.error_handler import FileAccessError

class FilePicker:
    def __init__(self, initial_dir: str):
        """Initialize file picker.
        
        Args:
            initial_dir: Initial directory to show in file picker
        """
        self.initial_dir = initial_dir
        
        # Ensure initial directory exists
        if not os.path.exists(initial_dir):
            try:
                os.makedirs(initial_dir)
            except Exception as e:
                raise FileAccessError(f"Failed to create initial directory: {str(e)}")

    def pick_file(self) -> Optional[str]:
        """Show file picker dialog for .txt files.
        
        Returns:
            Selected file path or None if cancelled
        """
        root = tk.Tk()
        root.withdraw()  # Hide the main window
        
        try:
            file_path = filedialog.askopenfilename(
                initialdir=self.initial_dir,
                title="Select Transcript File",
                filetypes=[("Text Files", "*.txt")]
            )
            
            if file_path:
                if not os.path.exists(file_path):
                    raise FileAccessError(f"Selected file does not exist: {file_path}")
                return file_path
            return None
            
        except Exception as e:
            raise FileAccessError(f"Error picking file: {str(e)}")
        finally:
            root.destroy()

    def read_file_content(self, file_path: str) -> str:
        """Read content of selected file.
        
        Args:
            file_path: Path to file to read
            
        Returns:
            File content as string
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            if not content.strip():
                raise FileAccessError("Selected file is empty")
                
            return content
        except Exception as e:
            raise FileAccessError(f"Failed to read file: {str(e)}")
