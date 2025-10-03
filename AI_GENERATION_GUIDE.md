# 🤖 AI Script Generation Guide

This guide shows you how to use AI assistants (ChatGPT, Claude, Gemini, etc.) to generate Automation Studio scripts.

---

## 🎯 Quick Start

### Step 1: Gather Information

Use Automation Studio's Coordinate Picker to capture screen positions:

```bash
python src/ui/main_window.py
# Click "🎯 Pick Coordinate" button
```

**What to collect:**
- 📍 Coordinates of buttons, fields, etc.
- ⌨️ Text you need to type
- ⏱️ Timing requirements
- 🔄 Sequence of actions

### Step 2: Create AI Prompt

Use this template:

````
I need an Automation Studio script in YAML format. Here's what it should do:

[Describe your automation task in plain English]

Coordinates I captured:
- Button at (500, 300)
- Text field at (600, 400)
- Submit button at (700, 600)

Text to type:
- Field 1: "username@example.com"
- Field 2: "SecurePass123"

Please generate a script using this YAML structure:

```yaml
name: Script Name
description: What it does
steps:
  - action: action_type
    [required parameters]
    description: What this step does
```

Available actions: click, double_click, type, hotkey, delay, paste, set_clipboard, press, scroll
````

### Step 3: Get AI Response

Send your prompt to your preferred AI assistant. The AI will generate YAML code.

### Step 4: Import & Test

1. Copy the AI-generated YAML
2. Save as `my_script.yaml`
3. Open in Automation Studio: "📂 Open Script"
4. Test with "▶️ Play Script"

---

## 📋 Prompt Templates

### Template 1: Simple Task Automation

````
Create an Automation Studio YAML script for this task:

Task: [Describe what you want to automate]

Steps:
1. [First action with details]
2. [Second action with details]
3. [Continue...]

Coordinates:
- Element 1: (X1, Y1) - [what it is]
- Element 2: (X2, Y2) - [what it is]

Format requirements:
- Use YAML syntax
- Each step needs: action, required parameters, and description
- Add appropriate delays between actions (suggest timing)
````

### Template 2: Form Filling

````
Generate an Automation Studio script to fill out this form:

Form fields and coordinates:
1. Name field at (X, Y) - enter "[name]"
2. Email field at (X, Y) - enter "[email]"
3. Phone field at (X, Y) - enter "[phone]"
4. Submit button at (X, Y)

Requirements:
- Use Tab key to move between fields (or click coordinates)
- Add 500ms delay between each field
- Add 1000ms delay before submitting

Format: YAML with steps list
Available actions: click, type, press (for Tab), delay, hotkey
````

### Template 3: Data Entry/Copy-Paste

````
Create an Automation Studio script for repetitive data entry:

Workflow:
1. Click data source at (X1, Y1)
2. Select item (double-click at X2, Y2)
3. Copy with Ctrl+C
4. Switch to target window (click at X3, Y3)
5. Paste with Ctrl+V
6. Save with Ctrl+S
7. Wait for save (2 seconds)

Generate YAML script with proper delays and descriptions for each step.
````

### Template 4: Complex Multi-Step

````
Create an Automation Studio YAML script for this complex workflow:

Background: [Explain what application/process]

Detailed steps:
1. [Action 1] at coordinates (X, Y) - [details]
2. Wait [duration] for [reason]
3. [Action 2] with text "[text content]"
4. [Continue with all steps...]

Special requirements:
- [Any specific timing needs]
- [Any repeated actions]
- [Error handling considerations]

Please include:
- Descriptive step descriptions
- Appropriate delays
- Comments explaining each section
````

---

## 🎨 Example Prompts & Responses

### Example 1: Login Automation

**Prompt:**
```
Create an Automation Studio YAML script to automate login:

1. Click username field at (850, 350)
2. Type "user@example.com"
3. Press Tab to move to password field
4. Type "MyPassword123"
5. Click login button at (850, 500)
6. Wait 3 seconds for login to complete

Add 500ms delays between actions. Use YAML format.
```

**Expected AI Response:**
```yaml
name: Website Login Automation
description: Automates the login process
version: 1.0

steps:
  - action: click
    x: 850
    y: 350
    description: Click username field

  - action: delay
    milliseconds: 500
    description: Wait for field to focus

  - action: type
    text: user@example.com
    description: Enter username

  - action: press
    key: tab
    presses: 1
    description: Move to password field

  - action: delay
    milliseconds: 500

  - action: type
    text: MyPassword123
    description: Enter password

  - action: delay
    milliseconds: 500

  - action: click
    x: 850
    y: 500
    description: Click login button

  - action: delay
    milliseconds: 3000
    description: Wait for login to complete
```

### Example 2: Data Collection

**Prompt:**
```
Generate Automation Studio script for collecting data:

1. Click record #1 at (400, 300)
2. Double-click name field at (450, 350) to select
3. Copy with Ctrl+C
4. Click spreadsheet window at (900, 200)
5. Click cell A1 at (920, 250)
6. Paste with Ctrl+V
7. Press Enter to move to next cell

Add appropriate delays. YAML format.
```

**Expected AI Response:**
```yaml
name: Data Collection Script
description: Copies data from records to spreadsheet
version: 1.0

steps:
  - action: click
    x: 400
    y: 300
    description: Select record #1

  - action: delay
    milliseconds: 300

  - action: double_click
    x: 450
    y: 350
    description: Select name field text

  - action: delay
    milliseconds: 300

  - action: hotkey
    keys: [ctrl, c]
    description: Copy selected text

  - action: delay
    milliseconds: 500

  - action: click
    x: 900
    y: 200
    description: Switch to spreadsheet window

  - action: delay
    milliseconds: 500

  - action: click
    x: 920
    y: 250
    description: Click cell A1

  - action: delay
    milliseconds: 300

  - action: paste
    description: Paste copied data

  - action: delay
    milliseconds: 300

  - action: press
    key: enter
    presses: 1
    description: Move to next cell
```

---

## 💡 Tips for Better AI Generation

### Be Specific
❌ Bad: "Make a script to fill a form"
✅ Good: "Create script to fill 3 fields at coordinates (X,Y) with specific text, then submit"

### Provide Context
Include:
- What application you're automating
- What each coordinate points to
- Expected timing/delays
- Any error handling needs

### Include Coordinates
Always provide exact coordinates from Coordinate Picker:
```
Button coordinates: (1200, 500)
Field coordinates: (1150, 350)
```

### Specify Timing
```
- Wait 500ms after clicking field
- Wait 2 seconds for page to load
- 100ms delay between keystrokes
```

### Request Descriptions
Ask AI to add descriptions to each step:
```
"Please add a description field to each step explaining what it does"
```

### Ask for Validation
```
"Make sure the YAML is valid and follows Automation Studio format"
```

---

## 🔄 Iteration Workflow

1. **Generate Initial Script**
   - Send prompt to AI
   - Get YAML response

2. **Test in Automation Studio**
   - Import script
   - Run and observe

3. **Identify Issues**
   - Note what failed
   - Check execution log

4. **Refine Prompt**
   - Add more details about issues
   - Request specific adjustments

5. **Regenerate**
   - Send updated prompt
   - Test again

### Example Refinement

**Initial Prompt:**
```
Create script to click button at (500, 300) and type "Hello"
```

**After Testing - Refinement:**
```
The button click was too fast. Update the script to:
- Click at (500, 300)
- Wait 1 second (1000ms)
- Type "Hello" with 100ms between each character
```

---

## 📚 Action Reference for AI

Share this with AI when generating scripts:

```yaml
# Mouse Actions
- action: click           # Single click
  x: 500
  y: 300

- action: double_click    # Double click
  x: 500
  y: 300

- action: right_click     # Right click
  x: 500
  y: 300

- action: move_to         # Move mouse
  x: 500
  y: 300
  duration: 0.5          # Optional

# Keyboard Actions
- action: type            # Type text
  text: "Hello World"
  interval: 0            # Optional: seconds between keys

- action: hotkey          # Key combination
  keys: [ctrl, c]        # Common: [ctrl,c], [ctrl,v], [alt,tab]

- action: press           # Press single key
  key: enter             # Common: enter, tab, escape, backspace
  presses: 1             # Optional

# Timing
- action: delay           # Wait
  milliseconds: 1000     # 1000 = 1 second

# Clipboard
- action: set_clipboard   # Set clipboard content
  text: "Text to copy"

- action: paste           # Paste (Ctrl+V)

# Other
- action: scroll          # Scroll
  amount: -3             # Negative=down, Positive=up
  x: 500                 # Optional
  y: 400                 # Optional

- action: screenshot      # Take screenshot
  filename: "shot.png"   # Optional
```

---

## 🎯 AI Platforms Tested

### ChatGPT (GPT-4/3.5)
✅ Excellent YAML generation
✅ Understands context well
✅ Good at suggesting delays

### Claude (Anthropic)
✅ Very detailed descriptions
✅ Asks clarifying questions
✅ Validates syntax

### Gemini (Google)
✅ Fast generation
✅ Good at following templates
✅ Handles complex workflows

### GitHub Copilot
✅ Great for code editing
✅ Auto-completes steps
⚠️ Best with examples

---

## 🚀 Advanced: Bulk Script Generation

### Generate Multiple Variations

**Prompt:**
```
Generate 3 Automation Studio scripts:

1. Fast version (minimal delays)
2. Normal version (500ms delays)
3. Safe version (1000ms+ delays)

Task: [Your automation task]
Coordinates: [Your coordinates]

Format each as separate YAML blocks.
```

### Generate Script Templates

**Prompt:**
```
Create a reusable Automation Studio script template for form filling.

Include:
- Placeholder comments for coordinates
- Variable delay options
- Common form actions (name, email, phone, submit)
- Instructions for customization

Format as YAML with comments.
```

---

## ✅ Validation Checklist

Before using AI-generated scripts:

- [ ] YAML syntax is valid
- [ ] All `action` fields are present
- [ ] Required parameters for each action type included
- [ ] Coordinates make sense for your screen
- [ ] Delays are appropriate
- [ ] Descriptions explain each step
- [ ] Script has `name` and `description`

---

## 📞 Getting Help

If AI-generated script doesn't work:

1. **Check YAML syntax** - Use "✓ Validate" in Code Editor
2. **Test coordinates** - Use Coordinate Picker to verify
3. **Check execution log** - See what's failing
4. **Adjust timing** - Add more delays
5. **Regenerate** - Send refined prompt to AI

---

**Pro Tip:** Keep a collection of working prompts for future use! 🎯

