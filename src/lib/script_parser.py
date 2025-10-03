"""
Script Parser and Validator

Parses automation scripts written in YAML format.
"""

import yaml
from typing import Dict, List, Any, Optional
from pathlib import Path


class ScriptParser:
    """Handles parsing and validation of automation scripts."""
    
    VALID_ACTIONS = {
        'click', 'double_click', 'right_click',
        'type', 'hotkey', 'press',
        'delay', 'wait',
        'move_to', 'drag_to',
        'scroll',
        'set_clipboard', 'paste',
        'screenshot',
        'message', 'input'
    }
    
    def __init__(self):
        """Initialize the script parser."""
        self.script_data: Optional[Dict] = None
        self.errors: List[str] = []
    
    def parse_file(self, file_path: str) -> bool:
        """
        Parse a script file.
        
        Args:
            file_path: Path to the YAML script file
            
        Returns:
            True if parsing successful, False otherwise
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                self.script_data = yaml.safe_load(f)
            
            return self.validate()
            
        except FileNotFoundError:
            self.errors.append(f"File not found: {file_path}")
            return False
        except yaml.YAMLError as e:
            self.errors.append(f"YAML parsing error: {str(e)}")
            return False
        except Exception as e:
            self.errors.append(f"Error parsing file: {str(e)}")
            return False
    
    def parse_string(self, script_content: str) -> bool:
        """
        Parse a script from string.
        
        Args:
            script_content: YAML script content as string
            
        Returns:
            True if parsing successful, False otherwise
        """
        try:
            self.script_data = yaml.safe_load(script_content)
            return self.validate()
            
        except yaml.YAMLError as e:
            self.errors.append(f"YAML parsing error: {str(e)}")
            return False
        except Exception as e:
            self.errors.append(f"Error parsing script: {str(e)}")
            return False
    
    def validate(self) -> bool:
        """
        Validate the parsed script data.
        
        Returns:
            True if valid, False otherwise
        """
        self.errors.clear()
        
        if not self.script_data:
            self.errors.append("Script data is empty")
            return False
        
        # Check required fields
        if 'name' not in self.script_data:
            self.errors.append("Missing required field: 'name'")
        
        if 'steps' not in self.script_data:
            self.errors.append("Missing required field: 'steps'")
            return False
        
        # Validate steps
        steps = self.script_data.get('steps', [])
        
        if not isinstance(steps, list):
            self.errors.append("'steps' must be a list")
            return False
        
        if len(steps) == 0:
            self.errors.append("'steps' cannot be empty")
            return False
        
        # Validate each step
        for i, step in enumerate(steps, 1):
            self._validate_step(step, i)
        
        return len(self.errors) == 0
    
    def _validate_step(self, step: Dict[str, Any], step_number: int) -> None:
        """
        Validate a single step.
        
        Args:
            step: Step dictionary
            step_number: Step number for error reporting
        """
        if not isinstance(step, dict):
            self.errors.append(f"Step {step_number}: Must be a dictionary")
            return
        
        if 'action' not in step:
            self.errors.append(f"Step {step_number}: Missing 'action' field")
            return
        
        action = step['action']
        
        if action not in self.VALID_ACTIONS:
            self.errors.append(
                f"Step {step_number}: Invalid action '{action}'. "
                f"Valid actions: {', '.join(sorted(self.VALID_ACTIONS))}"
            )
        
        # Validate action-specific requirements
        if action in ['click', 'double_click', 'right_click', 'move_to']:
            if 'x' not in step or 'y' not in step:
                self.errors.append(
                    f"Step {step_number}: Action '{action}' requires 'x' and 'y' coordinates"
                )
        
        elif action == 'type':
            if 'text' not in step:
                self.errors.append(
                    f"Step {step_number}: Action 'type' requires 'text' field"
                )
        
        elif action == 'hotkey':
            if 'keys' not in step:
                self.errors.append(
                    f"Step {step_number}: Action 'hotkey' requires 'keys' field"
                )
            elif not isinstance(step['keys'], list):
                self.errors.append(
                    f"Step {step_number}: 'keys' must be a list"
                )
        
        elif action in ['delay', 'wait']:
            if 'milliseconds' not in step:
                self.errors.append(
                    f"Step {step_number}: Action '{action}' requires 'milliseconds' field"
                )
        
        elif action == 'scroll':
            if 'amount' not in step:
                self.errors.append(
                    f"Step {step_number}: Action 'scroll' requires 'amount' field"
                )
    
    def get_script_data(self) -> Optional[Dict]:
        """
        Get the parsed script data.
        
        Returns:
            Script data dictionary or None
        """
        return self.script_data
    
    def get_errors(self) -> List[str]:
        """
        Get validation errors.
        
        Returns:
            List of error messages
        """
        return self.errors
    
    def get_metadata(self) -> Dict[str, Any]:
        """
        Get script metadata.
        
        Returns:
            Dictionary with metadata
        """
        if not self.script_data:
            return {}
        
        return {
            'name': self.script_data.get('name', 'Untitled'),
            'description': self.script_data.get('description', ''),
            'author': self.script_data.get('author', ''),
            'version': self.script_data.get('version', '1.0'),
            'step_count': len(self.script_data.get('steps', []))
        }

