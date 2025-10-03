# ⚡ Quick Start Guide

Get started with Automation Studio in 5 minutes!

---

## 🚀 Installation

```bash
cd automation-studio
pip install -r requirements.txt
```

---

## 🎬 Launch the App

```bash
python app.py
```

Or:

```bash
python src/ui/main_window.py
```

---

## 📝 Create Your First Automation

### Method 1: Visual Builder (Recommended)

1. **Launch the app** (see above)

2. **Fill script info:**
   - Name: "My First Script"
   - Description: "Learning automation"

3. **Add steps:**
   - Click "➕ Add Step"
   - Choose "🖱️ Click"
   - Click "🎯 Pick Coordinate" to capture screen position
   - Fill X, Y coordinates
   - Add description: "Click button"
   - Click OK

4. **Add more steps:**
   - Click "➕ Add Step" again
   - Choose "⏱️ Delay/Wait"
   - Enter 1000 milliseconds
   - Add description: "Wait 1 second"

5. **Add typing:**
   - Click "➕ Add Step"
   - Choose "⌨️ Type Text"
   - Enter text: "Hello World"
   - Click OK

6. **Save script:**
   - Click "💾 Save"
   - Choose location
   - Save as `my_first_script.yaml`

7. **Run it:**
   - Click "▶️ Play Script"
   - Watch it run!
   - Emergency stop: Move mouse to top-left corner

### Method 2: AI Generation

1. **Collect coordinates:**
   - Launch app
   - Click "🎯 Pick Coordinate"
   - Wait 3 seconds, move mouse to target
   - Note the captured coordinates
   - Repeat for all elements you need

2. **Create prompt for AI (ChatGPT/Claude/Gemini):**
   ```
   Create an Automation Studio YAML script that:
   1. Clicks at (500, 300)
   2. Waits 1 second
   3. Types "Hello World"
   
   Use this format:
   name: Script Name
   steps:
     - action: click
       x: 500
       y: 300
     - action: delay
       milliseconds: 1000
     - action: type
       text: "Hello World"
   ```

3. **Get AI response and save:**
   - Copy the YAML code AI generates
   - Save as `my_script.yaml`

4. **Import and run:**
   - In Automation Studio, click "📂 Open Script"
   - Select your saved YAML file
   - Click "▶️ Play Script"

### Method 3: Use Example

1. **Open example:**
   - Click "📂 Open Script"
   - Navigate to `examples/`
   - Open `simple_example.yaml`

2. **Review the steps:**
   - See how actions are structured
   - Note the syntax

3. **Modify:**
   - Click "📝 Edit Code" to see YAML
   - Or use "✏️ Edit Step" to modify steps visually

4. **Save as your own:**
   - Click "💾 Save As..."
   - Give it a new name

---

## 🎯 Essential Features

### Coordinate Picker
**Capture screen positions easily!**

- Click "🎯 Pick Coordinate" button
- Wait 3 seconds
- Move mouse to target element
- Coordinates captured automatically
- Use in your steps

### Code Editor
**Edit YAML directly!**

- Click "📝 Edit Code"
- Edit script in YAML format
- Click "✓ Validate" to check syntax
- Save changes

### Script Player
**Run with controls!**

- ▶️ **Play** - Start execution
- ⏸️ **Pause** - Pause/Resume
- ⏹️ **Stop** - Stop completely
- **Progress bar** - See current step
- **Execution log** - Watch real-time output

### Step Management
**Organize your automation!**

- ➕ Add Step - Insert new actions
- ✏️ Edit Step - Modify existing
- 🗑️ Delete Step - Remove steps
- ⬆️⬇️ Move - Reorder steps

---

## 📚 Learn More

- **Full Documentation:** See [README.md](README.md)
- **AI Generation:** See [AI_GENERATION_GUIDE.md](AI_GENERATION_GUIDE.md)
- **Examples:** Check `examples/` folder

---

## 💡 Quick Tips

1. **Always test coordinates** - Screen positions may vary
2. **Add delays** - Give UI time to respond (500-1000ms)
3. **Use descriptions** - Helps you understand steps later
4. **Save often** - Don't lose your work
5. **Start simple** - Build complex automations step by step
6. **Use fail-safe** - Keep enabled during testing

---

## 🆘 Common Issues

**Script won't run?**
- Check YAML syntax with "✓ Validate"
- Look at execution log for errors
- Try running examples first

**Wrong click location?**
- Recapture coordinates with Coordinate Picker
- Ensure window is in same position
- Check screen resolution hasn't changed

**Actions too fast?**
- Add more delays between steps
- Increase delay values (1000ms → 2000ms)

**Can't find coordinates?**
- Use Coordinate Picker built into app
- Test coordinates with visual marker first
- Take screenshots as reference

---

## ✅ Next Steps

Once comfortable:

1. ✨ Try the example scripts
2. 🤖 Generate scripts with AI
3. 🔄 Automate your repetitive tasks
4. 📦 Share your scripts
5. 🚀 Build complex workflows

---

**You're ready! Start automating! 🎉**

