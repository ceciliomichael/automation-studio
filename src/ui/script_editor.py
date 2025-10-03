"""
Script Code Editor

Allows direct editing of script YAML code.
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import yaml
from typing import Optional, Dict, Any


class ScriptEditorDialog:
    """Dialog for editing script code directly."""
    
    def __init__(self, parent: tk.Tk, script_data: Dict[str, Any]):
        """
        Initialize script editor.
        
        Args:
            parent: Parent window
            script_data: Current script data
        """
        self.result: Optional[Dict[str, Any]] = None
        self.original_data = script_data
        
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Edit Script Code")
        self.dialog.geometry("800x600")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        self._create_widgets()
        self._setup_layout()
        self._load_script()
        
        # Center dialog
        self.dialog.update_idletasks()
        x = parent.winfo_x() + (parent.winfo_width() // 2) - (self.dialog.winfo_width() // 2)
        y = parent.winfo_y() + (parent.winfo_height() // 2) - (self.dialog.winfo_height() // 2)
        self.dialog.geometry(f"+{x}+{y}")
        
        self.dialog.wait_window()
    
    def _create_widgets(self) -> None:
        """Create widgets."""
        self.main_frame = ttk.Frame(self.dialog, padding="10")
        
        self.title_label = ttk.Label(
            self.main_frame,
            text="📝 Script Code Editor (YAML)",
            font=('Segoe UI', 12, 'bold')
        )
        
        self.info_label = ttk.Label(
            self.main_frame,
            text="Edit the script code directly. Make sure to maintain valid YAML syntax.",
            font=('Segoe UI', 9),
            foreground='gray'
        )
        
        self.editor_frame = ttk.Frame(self.main_frame)
        
        self.editor_scroll = ttk.Scrollbar(self.editor_frame)
        
        self.editor_text = scrolledtext.ScrolledText(
            self.editor_frame,
            width=80,
            height=30,
            font=('Consolas', 10),
            yscrollcommand=self.editor_scroll.set
        )
        self.editor_scroll.config(command=self.editor_text.yview)
        
        self.button_frame = ttk.Frame(self.main_frame)
        
        self.btn_validate = ttk.Button(
            self.button_frame,
            text="✓ Validate",
            command=self._validate,
            width=15
        )
        
        self.btn_ok = ttk.Button(
            self.button_frame,
            text="Save",
            command=self._ok,
            width=15
        )
        
        self.btn_cancel = ttk.Button(
            self.button_frame,
            text="Cancel",
            command=self._cancel,
            width=15
        )
    
    def _setup_layout(self) -> None:
        """Setup layout."""
        self.main_frame.pack(fill='both', expand=True)
        
        self.title_label.pack(pady=(0, 5))
        self.info_label.pack(pady=(0, 10))
        
        self.editor_frame.pack(fill='both', expand=True, pady=(0, 10))
        self.editor_text.pack(side='left', fill='both', expand=True)
        self.editor_scroll.pack(side='right', fill='y')
        
        self.button_frame.pack(fill='x')
        self.btn_validate.pack(side='left', padx=5)
        self.btn_ok.pack(side='right', padx=5)
        self.btn_cancel.pack(side='right')
    
    def _load_script(self) -> None:
        """Load script data into editor."""
        yaml_str = yaml.dump(self.original_data, default_flow_style=False, sort_keys=False)
        self.editor_text.insert('1.0', yaml_str)
    
    def _validate(self) -> None:
        """Validate the YAML syntax."""
        try:
            code = self.editor_text.get('1.0', 'end-1c')
            data = yaml.safe_load(code)
            
            # Basic validation
            if not isinstance(data, dict):
                messagebox.showerror("Validation Error", "Script must be a YAML dictionary", parent=self.dialog)
                return
            
            if 'steps' not in data:
                messagebox.showerror("Validation Error", "Script must have 'steps' field", parent=self.dialog)
                return
            
            if not isinstance(data['steps'], list):
                messagebox.showerror("Validation Error", "'steps' must be a list", parent=self.dialog)
                return
            
            messagebox.showinfo("Validation Success", "✓ Script is valid!", parent=self.dialog)
            
        except yaml.YAMLError as e:
            messagebox.showerror("YAML Error", f"Invalid YAML syntax:\n{str(e)}", parent=self.dialog)
        except Exception as e:
            messagebox.showerror("Error", f"Validation error:\n{str(e)}", parent=self.dialog)
    
    def _ok(self) -> None:
        """Handle Save button."""
        try:
            code = self.editor_text.get('1.0', 'end-1c')
            self.result = yaml.safe_load(code)
            
            # Basic validation
            if not isinstance(self.result, dict):
                raise ValueError("Script must be a YAML dictionary")
            
            if 'steps' not in self.result:
                raise ValueError("Script must have 'steps' field")
            
            self.dialog.destroy()
            
        except yaml.YAMLError as e:
            messagebox.showerror("YAML Error", f"Invalid YAML syntax:\n{str(e)}", parent=self.dialog)
        except Exception as e:
            messagebox.showerror("Error", f"Save error:\n{str(e)}", parent=self.dialog)
    
    def _cancel(self) -> None:
        """Handle Cancel button."""
        self.result = None
        self.dialog.destroy()

