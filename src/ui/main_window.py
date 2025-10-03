"""
Automation Studio - Main Window

User-friendly GUI for creating, editing, and running automation scripts.
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import threading
import sys
from pathlib import Path
import yaml
import keyboard

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.lib.script_parser import ScriptParser
from src.lib.script_executor import ScriptExecutor
from src.ui.coordinate_picker import CoordinatePickerDialog
from src.ui.script_editor import ScriptEditorDialog


class AutomationStudio:
    """Main application window for Automation Studio."""
    
    def __init__(self, root: tk.Tk):
        """
        Initialize Automation Studio.
        
        Args:
            root: Tkinter root window
        """
        self.root = root
        self.root.title("Automation Studio - Visual Script Builder")
        self.root.geometry("1400x900")
        
        self.current_script = None
        self.script_file_path = None
        self.executor = ScriptExecutor(fail_safe=True)
        self.is_modified = False
        self.hotkey_registered = False
        
        # Setup executor callbacks
        self.executor.on_step_start = self._on_step_start
        self.executor.on_step_complete = self._on_step_complete
        self.executor.on_script_complete = self._on_script_complete
        self.executor.on_error = self._on_error
        self.executor.on_log = self._log
        
        self._setup_styles()
        self._create_widgets()
        self._setup_layout()
        self._create_new_script()
        self._setup_hotkeys()
    
    def _setup_styles(self) -> None:
        """Configure ttk styles."""
        style = ttk.Style()
        style.theme_use('clam')
        
        style.configure('Title.TLabel', font=('Segoe UI', 16, 'bold'))
        style.configure('Accent.TButton', font=('Segoe UI', 10, 'bold'), padding=10)
    
    def _create_widgets(self) -> None:
        """Create all GUI widgets."""
        # Main container
        self.main_frame = ttk.Frame(self.root, padding="10")
        
        # Title bar
        self.title_bar = ttk.Frame(self.main_frame)
        self.title_label = ttk.Label(
            self.title_bar,
            text="🎬 Automation Studio",
            style='Title.TLabel'
        )
        self.subtitle_label = ttk.Label(
            self.title_bar,
            text="Visual Script Builder - Create automations with ease",
            font=('Segoe UI', 10, 'italic')
        )
        
        # Toolbar
        self.toolbar = ttk.Frame(self.main_frame)
        
        self.btn_new = ttk.Button(
            self.toolbar,
            text="📄 New Script",
            command=self._new_script,
            width=15
        )
        
        self.btn_open = ttk.Button(
            self.toolbar,
            text="📂 Open Script",
            command=self._open_script,
            width=15
        )
        
        self.btn_save = ttk.Button(
            self.toolbar,
            text="💾 Save",
            command=self._save_script,
            width=15
        )
        
        self.btn_save_as = ttk.Button(
            self.toolbar,
            text="💾 Save As...",
            command=self._save_script_as,
            width=15
        )
        
        ttk.Separator(self.toolbar, orient='vertical').grid(row=0, column=4, padx=10, sticky='ns')
        
        self.btn_pick_coord = ttk.Button(
            self.toolbar,
            text="🎯 Pick Coordinate",
            command=self._pick_coordinate,
            width=18
        )
        
        self.btn_edit_code = ttk.Button(
            self.toolbar,
            text="📝 Edit Code",
            command=self._edit_code,
            width=15
        )
        
        # Main content area
        self.content_paned = ttk.PanedWindow(self.main_frame, orient='horizontal')
        
        # Left panel - Script Info & Steps
        self.left_panel = ttk.Frame(self.content_paned)
        
        # Script metadata
        self.metadata_frame = ttk.LabelFrame(
            self.left_panel,
            text="Script Information",
            padding="10"
        )
        
        ttk.Label(self.metadata_frame, text="Name:", font=('Segoe UI', 9, 'bold')).grid(
            row=0, column=0, sticky='w', pady=5
        )
        self.script_name_entry = ttk.Entry(self.metadata_frame, width=40)
        self.script_name_entry.grid(row=0, column=1, sticky='ew', pady=5, padx=(5, 0))
        self.script_name_entry.bind('<KeyRelease>', lambda e: self._mark_modified())
        
        ttk.Label(self.metadata_frame, text="Description:", font=('Segoe UI', 9, 'bold')).grid(
            row=1, column=0, sticky='nw', pady=5
        )
        self.script_desc_text = tk.Text(self.metadata_frame, width=40, height=3, font=('Segoe UI', 9))
        self.script_desc_text.grid(row=1, column=1, sticky='ew', pady=5, padx=(5, 0))
        self.script_desc_text.bind('<KeyRelease>', lambda e: self._mark_modified())
        
        self.metadata_frame.columnconfigure(1, weight=1)
        
        # Steps list
        self.steps_frame = ttk.LabelFrame(
            self.left_panel,
            text="Automation Steps",
            padding="10"
        )
        
        self.steps_tree_frame = ttk.Frame(self.steps_frame)
        
        self.steps_scroll = ttk.Scrollbar(self.steps_tree_frame)
        
        self.steps_tree = ttk.Treeview(
            self.steps_tree_frame,
            columns=('Action', 'Details'),
            show='tree headings',
            height=20,
            yscrollcommand=self.steps_scroll.set
        )
        self.steps_scroll.config(command=self.steps_tree.yview)
        
        self.steps_tree.heading('#0', text='#')
        self.steps_tree.heading('Action', text='Action')
        self.steps_tree.heading('Details', text='Details')
        
        self.steps_tree.column('#0', width=50, minwidth=50)
        self.steps_tree.column('Action', width=150, minwidth=100)
        self.steps_tree.column('Details', width=400, minwidth=200, stretch=True)
        
        # Step controls
        self.steps_controls = ttk.Frame(self.steps_frame)
        
        self.btn_add_step = ttk.Button(
            self.steps_controls,
            text="+ Add Step",
            command=self._show_add_step_menu
        )
        
        self.btn_edit_step = ttk.Button(
            self.steps_controls,
            text="Edit Step",
            command=self._edit_step
        )
        
        self.btn_delete_step = ttk.Button(
            self.steps_controls,
            text="Delete Step",
            command=self._delete_step
        )
        
        self.btn_move_up = ttk.Button(
            self.steps_controls,
            text="↑ Move Up",
            command=self._move_step_up
        )
        
        self.btn_move_down = ttk.Button(
            self.steps_controls,
            text="↓ Move Down",
            command=self._move_step_down
        )
        
        # Right panel - Player & Log
        self.right_panel = ttk.Frame(self.content_paned)
        
        # Player controls
        self.player_frame = ttk.LabelFrame(
            self.right_panel,
            text="▶️ Script Player",
            padding="10"
        )
        
        self.player_controls = ttk.Frame(self.player_frame)
        
        self.btn_play = ttk.Button(
            self.player_controls,
            text="▶️ Play Script",
            command=self._play_script,
            style='Accent.TButton',
            width=15
        )
        
        self.btn_pause = ttk.Button(
            self.player_controls,
            text="⏸️ Pause",
            command=self._pause_script,
            state='disabled',
            width=15
        )
        
        self.btn_stop = ttk.Button(
            self.player_controls,
            text="⏹️ Stop",
            command=self._stop_script,
            state='disabled',
            width=15
        )
        
        # Progress
        self.progress_frame = ttk.Frame(self.player_frame)
        
        self.progress_label = ttk.Label(
            self.progress_frame,
            text="Ready",
            font=('Segoe UI', 10, 'bold'),
            foreground='green'
        )
        
        self.progress_bar = ttk.Progressbar(
            self.progress_frame,
            mode='determinate',
            length=400
        )
        
        self.progress_detail = ttk.Label(
            self.progress_frame,
            text="Step 0 of 0",
            font=('Segoe UI', 9)
        )
        
        # Fail-safe option
        self.failsafe_var = tk.BooleanVar(value=True)
        self.failsafe_check = ttk.Checkbutton(
            self.player_frame,
            text="Enable Fail-Safe (Move mouse to corner to abort)",
            variable=self.failsafe_var
        )
        
        # Log
        self.log_frame = ttk.LabelFrame(
            self.right_panel,
            text="📋 Execution Log",
            padding="10"
        )
        
        self.log_text = scrolledtext.ScrolledText(
            self.log_frame,
            width=60,
            height=25,
            font=('Consolas', 9),
            bg='#1e1e1e',
            fg='#d4d4d4',
            state='disabled'
        )
        
        self.btn_clear_log = ttk.Button(
            self.log_frame,
            text="Clear Log",
            command=self._clear_log
        )
        
        # Status bar
        self.status_bar = ttk.Frame(self.main_frame)
        self.status_label = ttk.Label(
            self.status_bar,
            text="Ready",
            relief='sunken',
            anchor='w'
        )
    
    def _setup_layout(self) -> None:
        """Arrange all widgets."""
        self.main_frame.grid(row=0, column=0, sticky='nsew')
        
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.rowconfigure(2, weight=1)
        
        # Title bar
        self.title_bar.grid(row=0, column=0, sticky='ew', pady=(0, 10))
        self.title_label.pack(side='left')
        self.subtitle_label.pack(side='left', padx=(20, 0))
        
        # Toolbar
        self.toolbar.grid(row=1, column=0, sticky='ew', pady=(0, 10))
        self.btn_new.grid(row=0, column=0, padx=2)
        self.btn_open.grid(row=0, column=1, padx=2)
        self.btn_save.grid(row=0, column=2, padx=2)
        self.btn_save_as.grid(row=0, column=3, padx=2)
        self.btn_pick_coord.grid(row=0, column=5, padx=2)
        self.btn_edit_code.grid(row=0, column=6, padx=2)
        
        # Content paned window
        self.content_paned.grid(row=2, column=0, sticky='nsew')
        self.content_paned.add(self.left_panel, weight=1)
        self.content_paned.add(self.right_panel, weight=1)
        
        # Left panel
        self.metadata_frame.pack(fill='x', pady=(0, 10))
        
        self.steps_frame.pack(fill='both', expand=True)
        self.steps_tree_frame.pack(fill='both', expand=True, pady=(0, 10))
        self.steps_tree.grid(row=0, column=0, sticky='nsew')
        self.steps_scroll.grid(row=0, column=1, sticky='ns')
        self.steps_tree_frame.rowconfigure(0, weight=1)
        self.steps_tree_frame.columnconfigure(0, weight=1)
        
        self.steps_controls.pack(fill='x')
        self.btn_add_step.pack(side='left', padx=2)
        self.btn_edit_step.pack(side='left', padx=2)
        self.btn_delete_step.pack(side='left', padx=2)
        self.btn_move_up.pack(side='left', padx=2)
        self.btn_move_down.pack(side='left', padx=2)
        
        # Right panel
        self.player_frame.pack(fill='x', pady=(0, 10))
        
        self.player_controls.pack(fill='x', pady=(0, 10))
        self.btn_play.pack(side='left', padx=5)
        self.btn_pause.pack(side='left', padx=5)
        self.btn_stop.pack(side='left', padx=5)
        
        self.progress_frame.pack(fill='x', pady=(0, 10))
        self.progress_label.pack(anchor='w')
        self.progress_bar.pack(fill='x', pady=5)
        self.progress_detail.pack(anchor='w')
        
        self.failsafe_check.pack(anchor='w')
        
        self.log_frame.pack(fill='both', expand=True)
        self.log_text.pack(fill='both', expand=True, pady=(0, 10))
        self.btn_clear_log.pack()
        
        # Status bar
        self.status_bar.grid(row=3, column=0, sticky='ew', pady=(10, 0))
        self.status_label.pack(fill='x')
    
    def _create_new_script(self) -> None:
        """Create a new empty script."""
        self.current_script = {
            'name': 'Untitled Script',
            'description': '',
            'author': '',
            'version': '1.0',
            'steps': []
        }
        self._update_ui_from_script()
        self.is_modified = False
        self.script_file_path = None
        self._update_title()
    
    def _new_script(self) -> None:
        """Handle new script button."""
        if self.is_modified:
            response = messagebox.askyesnocancel(
                "Save Changes?",
                "Do you want to save changes to the current script?"
            )
            if response is None:  # Cancel
                return
            elif response:  # Yes
                self._save_script()
        
        self._create_new_script()
        self._log("Created new script")
    
    def _open_script(self) -> None:
        """Open an existing script file."""
        file_path = filedialog.askopenfilename(
            title="Open Script",
            filetypes=[("YAML files", "*.yaml *.yml"), ("All files", "*.*")],
            defaultextension=".yaml"
        )
        
        if not file_path:
            return
        
        parser = ScriptParser()
        if parser.parse_file(file_path):
            self.current_script = parser.get_script_data()
            self.script_file_path = file_path
            self._update_ui_from_script()
            self.is_modified = False
            self._update_title()
            self._log(f"Opened script: {file_path}")
        else:
            errors = '\n'.join(parser.get_errors())
            messagebox.showerror("Parse Error", f"Failed to parse script:\n\n{errors}")
    
    def _save_script(self) -> None:
        """Save the current script."""
        if not self.script_file_path:
            self._save_script_as()
            return
        
        self._update_script_from_ui()
        
        try:
            with open(self.script_file_path, 'w', encoding='utf-8') as f:
                yaml.dump(self.current_script, f, default_flow_style=False, sort_keys=False)
            
            self.is_modified = False
            self._update_title()
            self._log(f"Saved script: {self.script_file_path}")
            messagebox.showinfo("Saved", "Script saved successfully!")
        except Exception as e:
            messagebox.showerror("Save Error", f"Failed to save script:\n{str(e)}")
    
    def _save_script_as(self) -> None:
        """Save the script with a new filename."""
        file_path = filedialog.asksaveasfilename(
            title="Save Script As",
            filetypes=[("YAML files", "*.yaml"), ("All files", "*.*")],
            defaultextension=".yaml"
        )
        
        if not file_path:
            return
        
        self.script_file_path = file_path
        self._save_script()
    
    def _update_ui_from_script(self) -> None:
        """Update UI widgets from current script data."""
        self.script_name_entry.delete(0, tk.END)
        self.script_name_entry.insert(0, self.current_script.get('name', ''))
        
        self.script_desc_text.delete('1.0', tk.END)
        self.script_desc_text.insert('1.0', self.current_script.get('description', ''))
        
        self._refresh_steps_tree()
    
    def _update_script_from_ui(self) -> None:
        """Update script data from UI widgets."""
        self.current_script['name'] = self.script_name_entry.get()
        self.current_script['description'] = self.script_desc_text.get('1.0', 'end-1c')
    
    def _refresh_steps_tree(self) -> None:
        """Refresh the steps tree view."""
        # Clear tree
        for item in self.steps_tree.get_children():
            self.steps_tree.delete(item)
        
        # Add steps
        steps = self.current_script.get('steps', [])
        for i, step in enumerate(steps, 1):
            action = step.get('action', 'unknown')
            details = self._format_step_details(step)
            self.steps_tree.insert('', 'end', text=str(i), values=(action, details))
    
    def _format_step_details(self, step: dict) -> str:
        """Format step details for display."""
        action = step.get('action')
        
        if action in ['click', 'double_click', 'right_click']:
            x, y = step.get('x', 0), step.get('y', 0)
            desc = step.get('description', '')
            return f"({x}, {y}) - {desc}" if desc else f"({x}, {y})"
        
        elif action == 'type':
            text = step.get('text', '')
            return f"{text[:50]}{'...' if len(text) > 50 else ''}"
        
        elif action == 'hotkey':
            keys = step.get('keys', [])
            return '+'.join(keys)
        
        elif action in ['delay', 'wait']:
            ms = step.get('milliseconds', 0)
            return f"{ms}ms"
        
        elif action == 'set_clipboard':
            text = step.get('text', '')
            return f"{text[:50]}{'...' if len(text) > 50 else ''}"
        
        else:
            desc = step.get('description', '')
            return desc if desc else str(step)
    
    def _show_add_step_menu(self) -> None:
        """Show menu for adding different types of steps."""
        menu = tk.Menu(self.root, tearoff=0)
        
        menu.add_command(label="Click", command=lambda: self._add_step_dialog('click'))
        menu.add_command(label="Double Click", command=lambda: self._add_step_dialog('double_click'))
        menu.add_command(label="Right Click", command=lambda: self._add_step_dialog('right_click'))
        menu.add_separator()
        menu.add_command(label="Type Text", command=lambda: self._add_step_dialog('type'))
        menu.add_command(label="Hotkey", command=lambda: self._add_step_dialog('hotkey'))
        menu.add_command(label="Press Key", command=lambda: self._add_step_dialog('press'))
        menu.add_separator()
        menu.add_command(label="Delay/Wait", command=lambda: self._add_step_dialog('delay'))
        menu.add_separator()
        menu.add_command(label="Set Clipboard", command=lambda: self._add_step_dialog('set_clipboard'))
        menu.add_command(label="Paste", command=lambda: self._add_step_dialog('paste'))
        
        menu.post(self.btn_add_step.winfo_rootx(), self.btn_add_step.winfo_rooty() + self.btn_add_step.winfo_height())
    
    def _add_step_dialog(self, action_type: str) -> None:
        """Show dialog to add a step."""
        from src.ui.step_dialog import StepDialog
        
        dialog = StepDialog(self.root, action_type)
        if dialog.result:
            self.current_script['steps'].append(dialog.result)
            self._refresh_steps_tree()
            self._mark_modified()
            self._log(f"Added step: {action_type}")
    
    def _edit_step(self) -> None:
        """Edit selected step."""
        selection = self.steps_tree.selection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a step to edit")
            return
        
        index = self.steps_tree.index(selection[0])
        step = self.current_script['steps'][index]
        
        from src.ui.step_dialog import StepDialog
        dialog = StepDialog(self.root, step['action'], step)
        
        if dialog.result:
            self.current_script['steps'][index] = dialog.result
            self._refresh_steps_tree()
            self._mark_modified()
            self._log(f"Edited step #{index + 1}")
    
    def _delete_step(self) -> None:
        """Delete selected step."""
        selection = self.steps_tree.selection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a step to delete")
            return
        
        index = self.steps_tree.index(selection[0])
        
        if messagebox.askyesno("Confirm Delete", f"Delete step #{index + 1}?"):
            del self.current_script['steps'][index]
            self._refresh_steps_tree()
            self._mark_modified()
            self._log(f"Deleted step #{index + 1}")
    
    def _move_step_up(self) -> None:
        """Move selected step up."""
        selection = self.steps_tree.selection()
        if not selection:
            return
        
        index = self.steps_tree.index(selection[0])
        if index == 0:
            return
        
        steps = self.current_script['steps']
        steps[index], steps[index - 1] = steps[index - 1], steps[index]
        self._refresh_steps_tree()
        self._mark_modified()
    
    def _move_step_down(self) -> None:
        """Move selected step down."""
        selection = self.steps_tree.selection()
        if not selection:
            return
        
        index = self.steps_tree.index(selection[0])
        steps = self.current_script['steps']
        
        if index >= len(steps) - 1:
            return
        
        steps[index], steps[index + 1] = steps[index + 1], steps[index]
        self._refresh_steps_tree()
        self._mark_modified()
    
    def _pick_coordinate(self) -> None:
        """Open coordinate picker dialog."""
        dialog = CoordinatePickerDialog(self.root)
        if dialog.result:
            x, y = dialog.result
            self._log(f"Coordinate captured: ({x}, {y}) - Ready to use in steps")
    
    def _edit_code(self) -> None:
        """Open code editor dialog."""
        self._update_script_from_ui()
        dialog = ScriptEditorDialog(self.root, self.current_script)
        
        if dialog.result:
            self.current_script = dialog.result
            self._update_ui_from_script()
            self._mark_modified()
    
    def _play_script(self) -> None:
        """Play/execute the script."""
        self._update_script_from_ui()
        
        # Validate
        parser = ScriptParser()
        parser.script_data = self.current_script
        
        if not parser.validate():
            errors = '\n'.join(parser.get_errors())
            messagebox.showerror("Validation Error", f"Script has errors:\n\n{errors}")
            return
        
        # Disable controls
        self.btn_play.config(state='disabled')
        self.btn_pause.config(state='normal')
        self.btn_stop.config(state='normal')
        self.progress_label.config(text="Running...", foreground='orange')
        
        # Update executor settings
        self.executor.fail_safe = self.failsafe_var.get()
        
        # Run in thread
        def run():
            self.executor.execute_script(self.current_script)
        
        threading.Thread(target=run, daemon=True).start()
    
    def _pause_script(self) -> None:
        """Pause script execution."""
        if self.executor.is_paused:
            self.executor.resume()
            self.btn_pause.config(text="⏸️ Pause")
        else:
            self.executor.pause()
            self.btn_pause.config(text="▶️ Resume")
    
    def _stop_script(self) -> None:
        """Stop script execution."""
        self.executor.stop()
        self._log("Stopping script execution...")
        # Schedule UI update after a short delay to ensure executor has stopped
        self.root.after(100, self._script_stopped)
    
    def _on_step_start(self, step_num: int, step: dict) -> None:
        """Callback when step starts."""
        total = self.executor.total_steps
        self.root.after(0, lambda: self._update_progress(step_num, total))
    
    def _on_step_complete(self, step_num: int, step: dict) -> None:
        """Callback when step completes."""
        pass
    
    def _on_script_complete(self) -> None:
        """Callback when script completes."""
        self.root.after(0, self._script_finished)
    
    def _on_error(self, error: str) -> None:
        """Callback on error."""
        self.root.after(0, lambda: self._script_error(error))
    
    def _update_progress(self, current: int, total: int) -> None:
        """Update progress bar."""
        self.progress_bar['maximum'] = total
        self.progress_bar['value'] = current
        self.progress_detail.config(text=f"Step {current} of {total}")
    
    def _script_finished(self) -> None:
        """Handle script completion."""
        self.btn_play.config(state='normal')
        self.btn_pause.config(state='disabled')
        self.btn_stop.config(state='disabled')
        self.btn_pause.config(text="⏸️ Pause")
        self.progress_label.config(text="Completed", foreground='green')
        messagebox.showinfo("Complete", "Script execution completed successfully!")
    
    def _script_stopped(self) -> None:
        """Handle script stop."""
        self.btn_play.config(state='normal')
        self.btn_pause.config(state='disabled')
        self.btn_stop.config(state='disabled')
        self.btn_pause.config(text="⏸️ Pause")
        self.progress_label.config(text="Stopped", foreground='red')
        self._log("Script execution stopped")
    
    def _script_error(self, error: str) -> None:
        """Handle script error."""
        self.btn_play.config(state='normal')
        self.btn_pause.config(state='disabled')
        self.btn_stop.config(state='disabled')
        self.btn_pause.config(text="⏸️ Pause")
        self.progress_label.config(text="Error", foreground='red')
        messagebox.showerror("Error", f"Script execution failed:\n{error}")
    
    def _log(self, message: str) -> None:
        """Log a message."""
        self.log_text.configure(state='normal')
        from datetime import datetime
        timestamp = datetime.now().strftime('%H:%M:%S')
        self.log_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.log_text.see(tk.END)
        self.log_text.configure(state='disabled')
    
    def _clear_log(self) -> None:
        """Clear the log."""
        self.log_text.configure(state='normal')
        self.log_text.delete('1.0', tk.END)
        self.log_text.configure(state='disabled')
    
    def _mark_modified(self) -> None:
        """Mark script as modified."""
        self.is_modified = True
        self._update_title()
    
    def _update_title(self) -> None:
        """Update window title."""
        name = self.current_script.get('name', 'Untitled')
        modified = " *" if self.is_modified else ""
        self.root.title(f"Automation Studio - {name}{modified}")
    
    def _setup_hotkeys(self) -> None:
        """Setup global hotkeys."""
        try:
            # Register CTRL+Q to stop automation
            keyboard.add_hotkey('ctrl+q', self._hotkey_stop_handler)
            self.hotkey_registered = True
            self._log("Hotkey registered: CTRL+Q to stop automation")
        except Exception as e:
            self._log(f"Failed to register hotkey: {str(e)}")
    
    def _hotkey_stop_handler(self) -> None:
        """Handle CTRL+Q hotkey press."""
        if self.executor.is_running:
            self._log("CTRL+Q pressed - Stopping automation")
            self.root.after(0, self._stop_script)
    
    def _cleanup_hotkeys(self) -> None:
        """Cleanup hotkeys on exit."""
        if self.hotkey_registered:
            try:
                keyboard.unhook_all_hotkeys()
            except:
                pass


def main():
    """Main entry point."""
    root = tk.Tk()
    app = AutomationStudio(root)
    
    # Setup cleanup on window close
    def on_closing():
        app._cleanup_hotkeys()
        root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    
    # Center window
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')
    
    root.mainloop()


if __name__ == "__main__":
    main()

