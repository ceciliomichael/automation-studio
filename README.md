## 🎬 Automation Studio

**Visual Script Builder for Desktop Automation**

Create, edit, and run automation scripts with an intuitive GUI. No programming required!

---

## ✨ Features

### 🎨 **User-Friendly GUI**
- Visual script builder with drag-and-drop interface
- Step-by-step automation creation
- Real-time script editing and preview

### 📝 **Simple YAML Syntax**
- Easy-to-read script format
- AI-friendly for generation (works with ChatGPT, Claude, Gemini, etc.)
- Import/Export scripts

### 🎯 **Built-in Tools**
- **Coordinate Picker**: Capture screen coordinates visually
- **Code Editor**: Edit scripts directly in YAML
- **Script Player**: Run scripts with play/pause/stop controls
- **Execution Log**: Real-time feedback during automation

### 🖱️ **Supported Actions**
- **Mouse**: Click, Double-Click, Right-Click, Move, Drag
- **Keyboard**: Type text, Hotkeys, Press keys
- **Timing**: Delays and waits
- **Clipboard**: Set, Paste
- **More**: Scroll, Screenshots, User prompts

---

## 📦 Installation

### Requirements
- Python 3.11+
- Windows 10/11 (or Linux/Mac with adjustments)

### Setup

```bash
cd automation-studio
pip install -r requirements.txt
```

---

## 🚀 Quick Start

### Launch Automation Studio

```bash
python src/ui/main_window.py
```

### Create Your First Script

1. **Launch the app** - Run the command above
2. **Add steps** - Click "➕ Add Step" and choose an action
3. **Use Coordinate Picker** - Click "🎯 Pick Coordinate" to capture screen positions
4. **Save script** - Click "💾 Save" to export as YAML
5. **Run it** - Click "▶️ Play Script" to execute

---

## 📖 Script Syntax

### Basic Structure

```yaml
name: My Automation Script
description: What this script does
author: Your Name
version: 1.0

steps:
  - action: click
    x: 500
    y: 300
    description: Click the button
  
  - action: delay
    milliseconds: 1000
    description: Wait 1 second
  
  - action: type
    text: Hello World
    description: Type some text
```

### Available Actions

#### 🖱️ Mouse Actions

**Click**
```yaml
- action: click
  x: 500
  y: 300
  description: Click at coordinates
```

**Double Click**
```yaml
- action: double_click
  x: 500
  y: 300
```

**Right Click**
```yaml
- action: right_click
  x: 500
  y: 300
```

**Move To**
```yaml
- action: move_to
  x: 500
  y: 300
  duration: 0.5  # Optional: seconds to move
```

**Drag To**
```yaml
- action: drag_to
  x: 600
  y: 400
  duration: 0.5
```

#### ⌨️ Keyboard Actions

**Type Text**
```yaml
- action: type
  text: Hello, World!
  interval: 0  # Optional: seconds between each character
```

**Hotkey (Key Combination)**
```yaml
- action: hotkey
  keys: [ctrl, c]  # Copy
  description: Copy text
```

Common hotkeys:
- `[ctrl, c]` - Copy
- `[ctrl, v]` - Paste
- `[ctrl, a]` - Select All
- `[ctrl, s]` - Save
- `[ctrl, z]` - Undo
- `[alt, tab]` - Switch window
- `[win, d]` - Show desktop

**Press Key**
```yaml
- action: press
  key: enter
  presses: 1  # How many times to press
```

#### ⏱️ Timing

**Delay/Wait**
```yaml
- action: delay
  milliseconds: 1000  # 1 second
  description: Wait before next action
```

#### 📋 Clipboard

**Set Clipboard**
```yaml
- action: set_clipboard
  text: Text to copy
  description: Set clipboard content
```

**Paste**
```yaml
- action: paste
  description: Paste from clipboard (Ctrl+V)
```

#### 📜 Scroll

**Scroll**
```yaml
- action: scroll
  amount: -3  # Negative = down, Positive = up
  x: 500  # Optional: scroll at specific location
  y: 400
```

#### 📸 Screenshot

**Take Screenshot**
```yaml
- action: screenshot
  filename: my_screenshot.png  # Optional
  description: Capture screen
```

---

## 🤖 AI-Assisted Script Generation

### Workflow

1. **Collect Information**
   - Use the Coordinate Picker to capture screen positions
   - Note what text to type, keys to press, etc.
   - Take screenshots if helpful

2. **Ask AI to Generate Script**
   
   Example prompt for ChatGPT/Claude/Gemini:
   
   ```
   Create an Automation Studio script in YAML format that:
   1. Clicks at (500, 300)
   2. Waits 1 second
   3. Types "username@example.com"
   4. Presses Tab
   5. Types "password123"
   6. Clicks at (600, 500) to submit
   
   Use the YAML format with steps list, each step having an action field.
   ```

3. **Import Generated Script**
   - Copy AI's output
   - Save as `.yaml` file
   - Open in Automation Studio via "📂 Open Script"

4. **Test and Refine**
   - Use "📝 Edit Code" if needed
   - Test individual steps
   - Adjust coordinates/timing as needed

### Example AI Prompt Template

```
Create an Automation Studio YAML script that does the following:

Actions needed:
- Click button at coordinates (X, Y)
- Type: "[text]"
- Press hotkey: [keys]
- Wait: [duration]
- [other actions...]

Use this format:
name: [Script Name]
description: [What it does]
steps:
  - action: [action_type]
    [required fields]
    description: [what this step does]
```

---

## 📂 Example Scripts

Check the `examples/` folder:

- **simple_example.yaml** - Basic actions demo
- **form_filling.yaml** - Automated form entry
- **data_entry.yaml** - Copy-paste automation

### Run Examples

1. Open Automation Studio
2. Click "📂 Open Script"
3. Navigate to `examples/`
4. Select a script
5. Click "▶️ Play Script"

---

## 🎯 Tips & Best Practices

### Coordinates
- **Always test coordinates** after creating a script
- **Screen resolution matters** - Coordinates are absolute screen positions
- **Use descriptions** - Add description to each step for clarity
- **Window positioning** - Ensure target windows are in same position as when coordinates were captured

### Timing
- **Add delays** between fast actions to let UI respond
- **Wait after clicks** - UI elements may need time to appear
- **Network operations** - Use longer delays for operations that involve loading

### Debugging
- **Run step-by-step** - Test each action individually
- **Check execution log** - Monitor what's happening in real-time
- **Use fail-safe** - Keep enabled to abort by moving mouse to corner
- **Screenshots** - Add screenshot actions to debug visually

### Script Organization
- **Break into sections** - Use descriptions to mark workflow phases
- **Reusable scripts** - Create small scripts for common tasks
- **Version control** - Save different versions of scripts
- **Document coordinates** - Comment what each coordinate points to

---

## 🛡️ Safety Features

### Fail-Safe
- **Enabled by default** - Move mouse to top-left corner to abort
- **Instant stop** - Stops execution immediately
- **Can be disabled** - Uncheck in player settings (not recommended)

### Player Controls
- **⏸️ Pause** - Pause execution at any time
- **⏹️ Stop** - Stop execution completely
- **Execution Log** - Monitor every action in real-time

---

## 🔧 Advanced Usage

### Programmatic Execution

```python
from src.lib.script_parser import ScriptParser
from src.lib.script_executor import ScriptExecutor

# Parse script
parser = ScriptParser()
parser.parse_file('my_script.yaml')

if parser.validate():
    # Execute
    executor = ScriptExecutor(fail_safe=True)
    executor.execute_script(parser.get_script_data())
else:
    print("Errors:", parser.get_errors())
```

### Custom Callbacks

```python
executor = ScriptExecutor()

def on_step(step_num, step):
    print(f"Executing step {step_num}: {step['action']}")

executor.on_step_start = on_step
executor.execute_script(script_data)
```

---

## 🆘 Troubleshooting

### Script Won't Run
- Check YAML syntax (use "✓ Validate" button)
- Verify all required fields are present
- Check execution log for specific errors

### Wrong Click Locations
- Recapture coordinates using Coordinate Picker
- Ensure target window is in same position
- Check if screen resolution changed

### Actions Too Fast
- Add more delays between steps
- Increase delay values (e.g., 1000ms → 2000ms)

### Text Not Typing
- Click target field first before typing
- Add delay after click before type
- Check if correct window is focused

---

## 📝 License

MIT License - Free to use for personal and commercial projects.

---

## 🤝 Contributing

Feel free to extend this tool:
- Add new action types in `script_executor.py`
- Create UI improvements
- Share example scripts
- Report bugs and suggestions

---

## 📧 Support

For issues or questions:
- Check example scripts
- Review this documentation
- Test with simple scripts first

---

**Happy Automating! 🚀**

