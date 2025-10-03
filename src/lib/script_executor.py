"""
Script Executor Engine

Executes automation scripts parsed by ScriptParser.
"""

import pyautogui
import pyperclip
import time
from typing import Dict, Any, Optional, Callable
from datetime import datetime


class ScriptExecutor:
    """Executes automation scripts step by step."""
    
    def __init__(self, fail_safe: bool = True):
        """
        Initialize the script executor.
        
        Args:
            fail_safe: Enable PyAutoGUI fail-safe feature
        """
        pyautogui.FAILSAFE = fail_safe
        pyautogui.PAUSE = 0.1
        
        self.is_running = False
        self.is_paused = False
        self.current_step = 0
        self.total_steps = 0
        
        # Callbacks
        self.on_step_start: Optional[Callable] = None
        self.on_step_complete: Optional[Callable] = None
        self.on_script_complete: Optional[Callable] = None
        self.on_error: Optional[Callable] = None
        self.on_log: Optional[Callable] = None
    
    def execute_script(self, script_data: Dict[str, Any]) -> bool:
        """
        Execute an automation script.
        
        Args:
            script_data: Parsed script data dictionary
            
        Returns:
            True if execution successful, False otherwise
        """
        try:
            self.is_running = True
            self.current_step = 0
            
            steps = script_data.get('steps', [])
            self.total_steps = len(steps)
            
            self._log(f"Starting script: {script_data.get('name', 'Untitled')}")
            self._log(f"Total steps: {self.total_steps}")
            
            for i, step in enumerate(steps, 1):
                if not self.is_running:
                    self._log("Script execution stopped by user")
                    break
                
                # Handle pause
                while self.is_paused and self.is_running:
                    time.sleep(0.1)
                
                if not self.is_running:
                    break
                
                self.current_step = i
                
                if self.on_step_start:
                    self.on_step_start(i, step)
                
                self._log(f"Step {i}/{self.total_steps}: {step.get('action', 'unknown')}")
                
                # Execute the step
                success = self._execute_step(step, i)
                
                if not success:
                    self._log(f"Step {i} failed, stopping execution")
                    return False
                
                if self.on_step_complete:
                    self.on_step_complete(i, step)
            
            if self.is_running:
                self._log("Script execution completed successfully")
                if self.on_script_complete:
                    self.on_script_complete()
            
            return True
            
        except pyautogui.FailSafeException:
            self._log("FAIL-SAFE triggered! Mouse moved to corner.")
            if self.on_error:
                self.on_error("Fail-safe triggered")
            return False
            
        except Exception as e:
            self._log(f"Error during execution: {str(e)}")
            if self.on_error:
                self.on_error(str(e))
            return False
            
        finally:
            self.is_running = False
            self.is_paused = False
    
    def _execute_step(self, step: Dict[str, Any], step_number: int) -> bool:
        """
        Execute a single step.
        
        Args:
            step: Step dictionary
            step_number: Current step number
            
        Returns:
            True if successful, False otherwise
        """
        try:
            action = step.get('action')
            description = step.get('description', '')
            
            if description:
                self._log(f"  → {description}")
            
            # Mouse actions
            if action == 'click':
                x, y = step['x'], step['y']
                self._log(f"  Clicking at ({x}, {y})")
                pyautogui.click(x, y)
            
            elif action == 'double_click':
                x, y = step['x'], step['y']
                self._log(f"  Double-clicking at ({x}, {y})")
                pyautogui.doubleClick(x, y)
            
            elif action == 'right_click':
                x, y = step['x'], step['y']
                self._log(f"  Right-clicking at ({x}, {y})")
                pyautogui.rightClick(x, y)
            
            elif action == 'move_to':
                x, y = step['x'], step['y']
                duration = step.get('duration', 0)
                self._log(f"  Moving to ({x}, {y})")
                pyautogui.moveTo(x, y, duration=duration)
            
            elif action == 'drag_to':
                x, y = step['x'], step['y']
                duration = step.get('duration', 0.5)
                self._log(f"  Dragging to ({x}, {y})")
                pyautogui.dragTo(x, y, duration=duration)
            
            # Keyboard actions
            elif action == 'type':
                text = step['text']
                interval = step.get('interval', 0)
                self._log(f"  Typing: {text[:50]}{'...' if len(text) > 50 else ''}")
                pyautogui.write(text, interval=interval)
            
            elif action == 'hotkey':
                keys = step['keys']
                self._log(f"  Pressing hotkey: {'+'.join(keys)}")
                pyautogui.hotkey(*keys)
            
            elif action == 'press':
                key = step['key']
                presses = step.get('presses', 1)
                self._log(f"  Pressing key: {key} ({presses}x)")
                pyautogui.press(key, presses=presses)
            
            # Timing
            elif action in ['delay', 'wait']:
                ms = step['milliseconds']
                self._log(f"  Waiting {ms}ms")
                time.sleep(ms / 1000.0)
            
            # Scroll
            elif action == 'scroll':
                amount = step['amount']
                x = step.get('x')
                y = step.get('y')
                self._log(f"  Scrolling {amount}")
                if x is not None and y is not None:
                    pyautogui.scroll(amount, x=x, y=y)
                else:
                    pyautogui.scroll(amount)
            
            # Clipboard
            elif action == 'set_clipboard':
                text = step['text']
                self._log(f"  Setting clipboard: {text[:50]}{'...' if len(text) > 50 else ''}")
                pyperclip.copy(text)
            
            elif action == 'paste':
                self._log("  Pasting from clipboard")
                pyautogui.hotkey('ctrl', 'v')
            
            # Screenshot
            elif action == 'screenshot':
                filename = step.get('filename', f'screenshot_{datetime.now().strftime("%Y%m%d_%H%M%S")}.png')
                self._log(f"  Taking screenshot: {filename}")
                screenshot = pyautogui.screenshot()
                screenshot.save(filename)
            
            # User interaction
            elif action == 'message':
                message = step['text']
                self._log(f"  Showing message: {message}")
                # This would need GUI integration
                print(f"MESSAGE: {message}")
            
            elif action == 'input':
                prompt = step['prompt']
                self._log(f"  Requesting input: {prompt}")
                # This would need GUI integration
                print(f"INPUT NEEDED: {prompt}")
            
            else:
                self._log(f"  Unknown action: {action}")
                return False
            
            return True
            
        except KeyError as e:
            self._log(f"  ERROR: Missing required field: {e}")
            return False
        except Exception as e:
            self._log(f"  ERROR: {str(e)}")
            return False
    
    def stop(self) -> None:
        """Stop script execution."""
        self.is_running = False
        self.is_paused = False
        self._log("Stop requested")
    
    def pause(self) -> None:
        """Pause script execution."""
        self.is_paused = True
        self._log("Paused")
    
    def resume(self) -> None:
        """Resume script execution."""
        self.is_paused = False
        self._log("Resumed")
    
    def _log(self, message: str) -> None:
        """
        Log a message.
        
        Args:
            message: Message to log
        """
        if self.on_log:
            self.on_log(message)
        else:
            print(message)
    
    def get_progress(self) -> tuple[int, int]:
        """
        Get current progress.
        
        Returns:
            Tuple of (current_step, total_steps)
        """
        return (self.current_step, self.total_steps)

