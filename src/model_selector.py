"""Model selector UI for OpenWebUI automation."""

import tkinter as tk
import customtkinter as ctk
from typing import List, Optional, Callable
from tkinter import ttk
from src.utils.error_handler import ModelError

class ModelSelector:
    def __init__(
        self,
        models: List[str],
        default_model: str,
        last_used_model: Optional[str],
        on_select: Callable[[str], None]
    ):
        """Initialize model selector.
        
        Args:
            models: List of available models
            default_model: Default model name
            last_used_model: Last used model name (if any)
            on_select: Callback for model selection
        """
        if not models:
            raise ModelError("No models available")

        self.models = models
        self.default_model = default_model
        self.last_used_model = last_used_model
        self.on_select = on_select
        self.selected_model = None

        # Create and configure the window
        self.window = ctk.CTk()
        self.window.title("Select Model")
        self.window.geometry("400x500")
        
        # Set appearance mode
        ctk.set_appearance_mode("system")
        ctk.set_default_color_theme("blue")

        self._create_widgets()

    def _create_widgets(self):
        """Create and arrange UI widgets."""
        # Frame for quick actions
        quick_frame = ctk.CTkFrame(self.window)
        quick_frame.pack(fill="x", padx=10, pady=5)

        # Default model button
        default_btn = ctk.CTkButton(
            quick_frame,
            text=f"Use Default ({self.default_model})",
            command=lambda: self._handle_selection(self.default_model)
        )
        default_btn.pack(fill="x", padx=5, pady=5)

        # Separator
        separator = ttk.Separator(self.window, orient='horizontal')
        separator.pack(fill='x', padx=10, pady=10)

        # Label for list
        label = ctk.CTkLabel(
            self.window,
            text="Available Models:",
            font=("Helvetica", 14, "bold")
        )
        label.pack(pady=5)

        # Create frame for listbox and scrollbar
        list_frame = ctk.CTkFrame(self.window)
        list_frame.pack(fill="both", expand=True, padx=10, pady=5)

        # Scrollbar
        scrollbar = ctk.CTkScrollbar(list_frame)
        scrollbar.pack(side="right", fill="y")

        # Listbox for models
        self.listbox = tk.Listbox(
            list_frame,
            yscrollcommand=scrollbar.set,
            font=("Helvetica", 12),
            selectmode="single",
            activestyle="none"
        )
        self.listbox.pack(side="left", fill="both", expand=True)

        # Configure scrollbar
        scrollbar.configure(command=self.listbox.yview)

        # Populate listbox
        for model in self.models:
            self.listbox.insert(tk.END, model)

        # Highlight last used model if available
        if self.last_used_model and self.last_used_model in self.models:
            idx = self.models.index(self.last_used_model)
            self.listbox.selection_set(idx)
            self.listbox.see(idx)

        # Bind double-click and return key
        self.listbox.bind('<Double-Button-1>', self._on_double_click)
        self.listbox.bind('<Return>', self._on_double_click)

        # Cancel button
        cancel_btn = ctk.CTkButton(
            self.window,
            text="Cancel",
            command=self.window.destroy
        )
        cancel_btn.pack(pady=10)

    def _on_double_click(self, event):
        """Handle double-click or return key on listbox."""
        selection = self.listbox.curselection()
        if selection:
            model = self.models[selection[0]]
            self._handle_selection(model)

    def _handle_selection(self, model: str):
        """Handle model selection."""
        self.selected_model = model
        self.on_select(model)
        self.window.destroy()

    def show(self) -> Optional[str]:
        """Show the model selector dialog.
        
        Returns:
            Selected model name or None if cancelled
        """
        self.window.mainloop()
        return self.selected_model
