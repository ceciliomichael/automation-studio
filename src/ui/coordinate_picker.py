"""
Coordinate Picker Dialog

Captures mouse coordinates with live tracking and F2 hotkey.
"""

import tkinter as tk
from tkinter import ttk
import pyautogui
import threading
from typing import Optional, Tuple


class CoordinatePickerDialog:
    """Dialog for picking coordinates from the screen."""
    
    def __init__(self, parent: tk.Tk):
        """
        Initialize coordinate picker.
        
        Args:
            parent: Parent window
        """
        self.result: Optional[Tuple[int, int]] = None
        self.picker_running = False
        self.picker_thread = None
        
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Pick Coordinate")
        self.dialog.geometry("450x350")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        self._create_widgets()
        self._setup_layout()
        
        # Center dialog
        self.dialog.update_idletasks()
        x = parent.winfo_x() + (parent.winfo_width() // 2) - (self.dialog.winfo_width() // 2)
        y = parent.winfo_y() + (parent.winfo_height() // 2) - (self.dialog.winfo_height() // 2)
        self.dialog.geometry(f"+{x}+{y}")
        
        self.dialog.wait_window()
    
    def _create_widgets(self) -> None:
        """Create widgets."""
        self.main_frame = ttk.Frame(self.dialog, padding="15")
        
        self.title_label = ttk.Label(
            self.main_frame,
            text="Coordinate Picker",
            font=('Segoe UI', 14, 'bold')
        )
        
        self.instructions = ttk.Label(
            self.main_frame,
            text=(
                "1. Click 'Start Live Picker' button below\n"
                "2. Move your mouse to the target position\n"
                "3. Press F2 to capture the coordinates"
            ),
            justify='left',
            font=('Segoe UI', 10)
        )
        
        self.btn_capture = ttk.Button(
            self.main_frame,
            text="Start Live Picker",
            command=self._toggle_picker,
            width=30
        )
        
        self.status_label = ttk.Label(
            self.main_frame,
            text="Press F2 to capture",
            font=('Segoe UI', 9, 'italic'),
            foreground='gray'
        )
        
        self.coord_label = ttk.Label(
            self.main_frame,
            text="Move your mouse...",
            font=('Consolas', 12),
            foreground='blue'
        )
        
        self.captured_label = ttk.Label(
            self.main_frame,
            text="",
            font=('Segoe UI', 10, 'bold'),
            foreground='green'
        )
        
        self.button_frame = ttk.Frame(self.main_frame)
        
        self.btn_ok = ttk.Button(
            self.button_frame,
            text="Use This Coordinate",
            command=self._ok,
            state='disabled',
            width=20
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
        
        self.title_label.pack(pady=(0, 10))
        self.instructions.pack(pady=(0, 10))
        self.btn_capture.pack(pady=(0, 8))
        self.status_label.pack(pady=2)
        self.coord_label.pack(pady=3)
        self.captured_label.pack(pady=3)
        
        self.button_frame.pack(side='bottom', pady=(10, 0))
        self.btn_ok.pack(side='right', padx=5)
        self.btn_cancel.pack(side='right')
    
    def _toggle_picker(self) -> None:
        """Toggle live coordinate picker."""
        if self.picker_running:
            self._stop_picker()
        else:
            self._start_picker()
    
    def _start_picker(self) -> None:
        """Start live coordinate picker."""
        self.picker_running = True
        self.btn_capture.config(text="Stop Picking")
        self.status_label.config(text="Press F2 to capture", foreground='orange')
        self.coord_label.config(text="Move your mouse...", foreground='blue')
        self.captured_label.config(text="")
        
        # Bind F2 key
        self.dialog.bind('<F2>', self._capture_coordinate)
        
        def update_coordinates():
            """Update coordinates in real-time."""
            while self.picker_running:
                try:
                    pos = pyautogui.position()
                    self.dialog.after(0, lambda p=pos: self.coord_label.config(
                        text=f"X: {p.x}, Y: {p.y}"
                    ))
                    threading.Event().wait(0.05)  # Update every 50ms
                except:
                    break
            
            # Clear label when stopped
            self.dialog.after(0, lambda: self.coord_label.config(text="Ready to start..."))
        
        self.picker_thread = threading.Thread(target=update_coordinates, daemon=True)
        self.picker_thread.start()
    
    def _stop_picker(self) -> None:
        """Stop live coordinate picker."""
        if self.picker_running:
            self.picker_running = False
            self.btn_capture.config(text="Start Live Picker")
            self.status_label.config(text="Press F2 to capture", foreground='gray')
            self.dialog.unbind('<F2>')
    
    def _capture_coordinate(self, event=None) -> None:
        """Capture current mouse position."""
        pos = pyautogui.position()
        self.result = (pos.x, pos.y)
        
        # Visual feedback
        self.captured_label.config(
            text=f"✓ Captured: X: {pos.x}, Y: {pos.y}",
            foreground='green'
        )
        self.status_label.config(text="Coordinate captured!", foreground='green')
        
        # Enable OK button
        self.btn_ok.config(state='normal')
        
        # Stop picker
        self._stop_picker()
    
    def _ok(self) -> None:
        """Handle OK button."""
        if self.picker_running:
            self._stop_picker()
        self.dialog.destroy()
    
    def _cancel(self) -> None:
        """Handle Cancel button."""
        if self.picker_running:
            self._stop_picker()
        self.result = None
        self.dialog.destroy()

