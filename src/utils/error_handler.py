"""Error handling utility for OpenWebUI automation."""

import tkinter as tk
from tkinter import messagebox
from typing import Optional, Callable
from .logger import Logger

class ErrorHandler:
    def __init__(self):
        self.logger = Logger()

    def handle_error(
        self,
        error: Exception,
        title: str = "Error",
        message: Optional[str] = None,
        callback: Optional[Callable] = None
    ) -> None:
        """Handle an error by logging it and showing a dialog.
        
        Args:
            error: The exception that occurred
            title: Title for the error dialog
            message: Custom message to show (if None, uses str(error))
            callback: Optional callback to execute after error is acknowledged
        """
        error_message = message or str(error)
        self.logger.error(f"{title}: {error_message}")
        
        # Ensure we have a root window for the dialog
        root = tk.Tk()
        root.withdraw()  # Hide the root window
        
        messagebox.showerror(title, error_message)
        
        if callback:
            try:
                callback()
            except Exception as e:
                self.logger.error(f"Error in error callback: {str(e)}")
        
        root.destroy()

    def show_warning(
        self,
        message: str,
        title: str = "Warning"
    ) -> None:
        """Show a warning dialog and log it.
        
        Args:
            message: Warning message to show
            title: Title for the warning dialog
        """
        self.logger.warning(f"{title}: {message}")
        
        root = tk.Tk()
        root.withdraw()
        
        messagebox.showwarning(title, message)
        root.destroy()

class OpenWebUIError(Exception):
    """Base exception class for OpenWebUI automation errors."""
    pass

class ConfigurationError(OpenWebUIError):
    """Raised when there's an issue with configuration."""
    pass

class ConnectionError(OpenWebUIError):
    """Raised when there's an issue connecting to OpenWebUI."""
    pass

class AuthenticationError(OpenWebUIError):
    """Raised when there's an authentication issue."""
    pass

class FileAccessError(OpenWebUIError):
    """Raised when there's an issue accessing files."""
    pass

class ModelError(OpenWebUIError):
    """Raised when there's an issue with model selection or availability."""
    pass
