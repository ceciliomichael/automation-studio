"""
Step Dialog

Dialog for adding/editing automation steps.
"""

import tkinter as tk
from tkinter import ttk
from typing import Optional, Dict, Any
import pyautogui
import threading


class StepDialog:
    """Dialog for creating/editing automation steps."""
    
    def __init__(self, parent: tk.Tk, action_type: str, existing_step: Optional[Dict] = None):
        """
        Initialize step dialog.
        
        Args:
            parent: Parent window
            action_type: Type of action (click, type, etc.)
            existing_step: Existing step data for editing
        """
        self.result: Optional[Dict[str, Any]] = None
        self.action_type = action_type
        self.existing_step = existing_step
        
        # Initialize picker variables
        self.picker_running = False
        self.picker_thread = None
        
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(f"{'Edit' if existing_step else 'Add'} Step - {action_type}")
        self.dialog.geometry("500x400")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        self._create_widgets()
        self._setup_layout()
        
        if existing_step:
            self._load_existing()
        
        # Center dialog
        self.dialog.update_idletasks()
        x = parent.winfo_x() + (parent.winfo_width() // 2) - (self.dialog.winfo_width() // 2)
        y = parent.winfo_y() + (parent.winfo_height() // 2) - (self.dialog.winfo_height() // 2)
        self.dialog.geometry(f"+{x}+{y}")
        
        self.dialog.wait_window()
    
    def _create_widgets(self) -> None:
        """Create dialog widgets."""
        self.main_frame = ttk.Frame(self.dialog, padding="20")
        
        # Action type label
        self.action_label = ttk.Label(
            self.main_frame,
            text=f"Action: {self.action_type}",
            font=('Segoe UI', 12, 'bold')
        )
        
        # Description
        ttk.Label(self.main_frame, text="Description (optional):", font=('Segoe UI', 9, 'bold')).pack(anchor='w', pady=(10, 5))
        self.desc_entry = ttk.Entry(self.main_frame, width=50)
        self.desc_entry.pack(fill='x', pady=(0, 15))
        
        # Action-specific fields frame
        self.fields_frame = ttk.Frame(self.main_frame)
        
        # Create fields based on action type
        if self.action_type in ['click', 'double_click', 'right_click', 'move_to']:
            self._create_coordinate_fields()
        
        elif self.action_type == 'type':
            self._create_type_fields()
        
        elif self.action_type == 'hotkey':
            self._create_hotkey_fields()
        
        elif self.action_type == 'press':
            self._create_press_fields()
        
        elif self.action_type in ['delay', 'wait']:
            self._create_delay_fields()
        
        elif self.action_type == 'set_clipboard':
            self._create_clipboard_fields()
        
        elif self.action_type == 'paste':
            pass  # No additional fields needed
        
        elif self.action_type == 'scroll':
            self._create_scroll_fields()
        
        # Buttons
        self.button_frame = ttk.Frame(self.main_frame)
        
        self.btn_ok = ttk.Button(
            self.button_frame,
            text="OK",
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
        self.action_label.pack(anchor='w', pady=(0, 10))
        self.fields_frame.pack(fill='both', expand=True, pady=(0, 20))
        
        self.button_frame.pack(fill='x')
        self.btn_ok.pack(side='right', padx=5)
        self.btn_cancel.pack(side='right')
    
    def _create_coordinate_fields(self) -> None:
        """Create coordinate input fields."""
        coord_frame = ttk.Frame(self.fields_frame)
        coord_frame.pack(fill='x', pady=10)
        
        ttk.Label(coord_frame, text="X Coordinate:", font=('Segoe UI', 9, 'bold')).grid(row=0, column=0, sticky='w', pady=5)
        self.x_entry = ttk.Entry(coord_frame, width=15)
        self.x_entry.grid(row=0, column=1, sticky='w', padx=(10, 0), pady=5)
        
        ttk.Label(coord_frame, text="Y Coordinate:", font=('Segoe UI', 9, 'bold')).grid(row=1, column=0, sticky='w', pady=5)
        self.y_entry = ttk.Entry(coord_frame, width=15)
        self.y_entry.grid(row=1, column=1, sticky='w', padx=(10, 0), pady=5)
        
        # Coordinate picker button and display
        picker_frame = ttk.Frame(coord_frame)
        picker_frame.grid(row=2, column=0, columnspan=2, sticky='ew', pady=(10, 0))
        
        self.btn_pick_coord = ttk.Button(
            picker_frame,
            text="Pick Coordinate (Live)",
            command=self._start_live_picker,
            width=22
        )
        self.btn_pick_coord.pack(side='left', padx=(0, 10))
        
        self.live_coord_label = ttk.Label(
            picker_frame,
            text="",
            font=('Consolas', 10),
            foreground='blue'
        )
        self.live_coord_label.pack(side='left')
        
        # Instructions
        ttk.Label(
            coord_frame,
            text="Click 'Pick Coordinate' then press F2 to capture position",
            font=('Segoe UI', 8, 'italic'),
            foreground='gray'
        ).grid(row=3, column=0, columnspan=2, sticky='w', pady=(5, 0))
        
        if self.action_type in ['move_to', 'drag_to']:
            ttk.Label(coord_frame, text="Duration (seconds):", font=('Segoe UI', 9, 'bold')).grid(row=4, column=0, sticky='w', pady=5)
            self.duration_entry = ttk.Entry(coord_frame, width=15)
            self.duration_entry.insert(0, "0")
            self.duration_entry.grid(row=4, column=1, sticky='w', padx=(10, 0), pady=5)
    
    def _create_type_fields(self) -> None:
        """Create text typing fields."""
        ttk.Label(self.fields_frame, text="Text to Type:", font=('Segoe UI', 9, 'bold')).pack(anchor='w', pady=5)
        
        self.text_widget = tk.Text(self.fields_frame, width=50, height=10, font=('Consolas', 10))
        self.text_widget.pack(fill='both', expand=True, pady=5)
        
        ttk.Label(self.fields_frame, text="Interval between keys (seconds, 0 for instant):", font=('Segoe UI', 9)).pack(anchor='w', pady=5)
        self.interval_entry = ttk.Entry(self.fields_frame, width=15)
        self.interval_entry.insert(0, "0")
        self.interval_entry.pack(anchor='w')
    
    def _create_hotkey_fields(self) -> None:
        """Create hotkey fields."""
        ttk.Label(self.fields_frame, text="Enter keys (comma-separated):", font=('Segoe UI', 9, 'bold')).pack(anchor='w', pady=5)
        ttk.Label(self.fields_frame, text="Example: ctrl, c  or  ctrl, shift, s", font=('Segoe UI', 9, 'italic'), foreground='gray').pack(anchor='w')
        
        self.keys_entry = ttk.Entry(self.fields_frame, width=50)
        self.keys_entry.pack(fill='x', pady=10)
        
        ttk.Label(self.fields_frame, text="Common keys:", font=('Segoe UI', 9, 'bold')).pack(anchor='w', pady=(10, 5))
        
        keys_frame = ttk.Frame(self.fields_frame)
        keys_frame.pack(fill='x')
        
        common_keys = [
            ("Ctrl+C (Copy)", "ctrl, c"),
            ("Ctrl+V (Paste)", "ctrl, v"),
            ("Ctrl+A (Select All)", "ctrl, a"),
            ("Ctrl+S (Save)", "ctrl, s"),
            ("Enter", "enter"),
            ("Tab", "tab"),
        ]
        
        for i, (label, keys) in enumerate(common_keys):
            btn = ttk.Button(
                keys_frame,
                text=label,
                command=lambda k=keys: self.keys_entry.delete(0, tk.END) or self.keys_entry.insert(0, k)
            )
            btn.grid(row=i // 2, column=i % 2, padx=5, pady=5, sticky='ew')
        
        keys_frame.columnconfigure(0, weight=1)
        keys_frame.columnconfigure(1, weight=1)
    
    def _create_press_fields(self) -> None:
        """Create press key fields."""
        ttk.Label(self.fields_frame, text="Key to Press:", font=('Segoe UI', 9, 'bold')).pack(anchor='w', pady=5)
        self.key_entry = ttk.Entry(self.fields_frame, width=30)
        self.key_entry.pack(fill='x', pady=5)
        
        ttk.Label(self.fields_frame, text="Number of Presses:", font=('Segoe UI', 9, 'bold')).pack(anchor='w', pady=5)
        self.presses_entry = ttk.Entry(self.fields_frame, width=15)
        self.presses_entry.insert(0, "1")
        self.presses_entry.pack(anchor='w')
    
    def _create_delay_fields(self) -> None:
        """Create delay fields."""
        ttk.Label(self.fields_frame, text="Delay Duration (milliseconds):", font=('Segoe UI', 9, 'bold')).pack(anchor='w', pady=5)
        self.ms_entry = ttk.Entry(self.fields_frame, width=15)
        self.ms_entry.pack(anchor='w', pady=5)
        
        ttk.Label(self.fields_frame, text="Quick Presets:", font=('Segoe UI', 9, 'bold')).pack(anchor='w', pady=(10, 5))
        
        presets_frame = ttk.Frame(self.fields_frame)
        presets_frame.pack(fill='x')
        
        presets = [
            ("0.5 seconds", "500"),
            ("1 second", "1000"),
            ("2 seconds", "2000"),
            ("3 seconds", "3000"),
            ("5 seconds", "5000"),
        ]
        
        for i, (label, ms) in enumerate(presets):
            btn = ttk.Button(
                presets_frame,
                text=label,
                command=lambda m=ms: self.ms_entry.delete(0, tk.END) or self.ms_entry.insert(0, m)
            )
            btn.grid(row=i // 2, column=i % 2, padx=5, pady=5, sticky='ew')
        
        presets_frame.columnconfigure(0, weight=1)
        presets_frame.columnconfigure(1, weight=1)
    
    def _create_clipboard_fields(self) -> None:
        """Create clipboard fields."""
        ttk.Label(self.fields_frame, text="Text to Copy to Clipboard:", font=('Segoe UI', 9, 'bold')).pack(anchor='w', pady=5)
        
        self.text_widget = tk.Text(self.fields_frame, width=50, height=10, font=('Consolas', 10))
        self.text_widget.pack(fill='both', expand=True, pady=5)
    
    def _create_scroll_fields(self) -> None:
        """Create scroll fields."""
        ttk.Label(self.fields_frame, text="Scroll Amount (negative = down, positive = up):", font=('Segoe UI', 9, 'bold')).pack(anchor='w', pady=5)
        self.amount_entry = ttk.Entry(self.fields_frame, width=15)
        self.amount_entry.pack(anchor='w', pady=5)
    
    def _load_existing(self) -> None:
        """Load existing step data into fields."""
        if not self.existing_step:
            return
        
        # Description
        desc = self.existing_step.get('description', '')
        if desc:
            self.desc_entry.insert(0, desc)
        
        # Action-specific fields
        if self.action_type in ['click', 'double_click', 'right_click', 'move_to']:
            self.x_entry.insert(0, str(self.existing_step.get('x', '')))
            self.y_entry.insert(0, str(self.existing_step.get('y', '')))
            if hasattr(self, 'duration_entry'):
                self.duration_entry.delete(0, tk.END)
                self.duration_entry.insert(0, str(self.existing_step.get('duration', 0)))
        
        elif self.action_type == 'type':
            self.text_widget.insert('1.0', self.existing_step.get('text', ''))
            self.interval_entry.delete(0, tk.END)
            self.interval_entry.insert(0, str(self.existing_step.get('interval', 0)))
        
        elif self.action_type == 'hotkey':
            keys = self.existing_step.get('keys', [])
            self.keys_entry.insert(0, ', '.join(keys))
        
        elif self.action_type == 'press':
            self.key_entry.insert(0, self.existing_step.get('key', ''))
            self.presses_entry.delete(0, tk.END)
            self.presses_entry.insert(0, str(self.existing_step.get('presses', 1)))
        
        elif self.action_type in ['delay', 'wait']:
            self.ms_entry.insert(0, str(self.existing_step.get('milliseconds', '')))
        
        elif self.action_type == 'set_clipboard':
            self.text_widget.insert('1.0', self.existing_step.get('text', ''))
        
        elif self.action_type == 'scroll':
            self.amount_entry.insert(0, str(self.existing_step.get('amount', '')))
    
    def _ok(self) -> None:
        """Handle OK button."""
        try:
            step = {'action': self.action_type}
            
            # Description
            desc = self.desc_entry.get().strip()
            if desc:
                step['description'] = desc
            
            # Action-specific fields
            if self.action_type in ['click', 'double_click', 'right_click', 'move_to']:
                step['x'] = int(self.x_entry.get())
                step['y'] = int(self.y_entry.get())
                if hasattr(self, 'duration_entry'):
                    duration = float(self.duration_entry.get())
                    if duration > 0:
                        step['duration'] = duration
            
            elif self.action_type == 'type':
                step['text'] = self.text_widget.get('1.0', 'end-1c')
                interval = float(self.interval_entry.get())
                if interval > 0:
                    step['interval'] = interval
            
            elif self.action_type == 'hotkey':
                keys_str = self.keys_entry.get()
                keys = [k.strip() for k in keys_str.split(',')]
                step['keys'] = keys
            
            elif self.action_type == 'press':
                step['key'] = self.key_entry.get()
                step['presses'] = int(self.presses_entry.get())
            
            elif self.action_type in ['delay', 'wait']:
                step['milliseconds'] = int(self.ms_entry.get())
            
            elif self.action_type == 'set_clipboard':
                step['text'] = self.text_widget.get('1.0', 'end-1c')
            
            elif self.action_type == 'paste':
                pass  # No additional fields
            
            elif self.action_type == 'scroll':
                step['amount'] = int(self.amount_entry.get())
            
            self.result = step
            self.dialog.destroy()
            
        except ValueError as e:
            tk.messagebox.showerror("Invalid Input", f"Please check your input:\n{str(e)}", parent=self.dialog)
    
    def _cancel(self) -> None:
        """Handle Cancel button."""
        if hasattr(self, 'picker_running') and self.picker_running:
            self._stop_live_picker()
        self.dialog.destroy()
    
    def _start_live_picker(self) -> None:
        """Start live coordinate picker."""
        if self.picker_running:
            self._stop_live_picker()
            return
        
        self.picker_running = True
        self.btn_pick_coord.config(text="Stop Picking")
        
        # Bind F2 key globally
        self.dialog.bind('<F2>', self._capture_coordinate)
        
        def update_coordinates():
            """Update coordinates in real-time."""
            while self.picker_running:
                try:
                    pos = pyautogui.position()
                    self.dialog.after(0, lambda p=pos: self.live_coord_label.config(
                        text=f"X: {p.x}, Y: {p.y}"
                    ))
                    threading.Event().wait(0.05)  # Update every 50ms
                except:
                    break
            
            # Clear label when stopped
            self.dialog.after(0, lambda: self.live_coord_label.config(text=""))
        
        self.picker_thread = threading.Thread(target=update_coordinates, daemon=True)
        self.picker_thread.start()
    
    def _stop_live_picker(self) -> None:
        """Stop live coordinate picker."""
        if self.picker_running:
            self.picker_running = False
            self.btn_pick_coord.config(text="Pick Coordinate (Live)")
            self.dialog.unbind('<F2>')
    
    def _capture_coordinate(self, event=None) -> None:
        """Capture current mouse position and set it in the entry fields."""
        pos = pyautogui.position()
        
        # Update entry fields
        self.x_entry.delete(0, tk.END)
        self.x_entry.insert(0, str(pos.x))
        
        self.y_entry.delete(0, tk.END)
        self.y_entry.insert(0, str(pos.y))
        
        # Visual feedback
        self.live_coord_label.config(
            text=f"✓ Captured: X: {pos.x}, Y: {pos.y}",
            foreground='green'
        )
        
        # Stop picker
        self._stop_live_picker()
        
        # Reset color after 2 seconds
        self.dialog.after(2000, lambda: self.live_coord_label.config(foreground='blue'))

