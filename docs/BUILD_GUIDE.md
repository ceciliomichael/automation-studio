# Automation Studio - Build Guide

This guide explains how to build Automation Studio into a standalone Windows executable.

## Prerequisites

1. **Python 3.11** installed
2. **All dependencies** installed:
   ```bash
   pip install -r requirements.txt
   ```

## Build Options

### Option 1: Build as Folder (Recommended)

This creates a folder with the executable and all dependencies. **Faster startup time** and easier debugging.

```bash
python build.py
```

**Output:** `dist/AutomationStudio/AutomationStudio.exe`

**Advantages:**
- Fast startup time
- Smaller individual file sizes
- Easy to debug
- Example files accessible to users

**Disadvantages:**
- Must distribute entire folder
- More files to manage

---

### Option 2: Build as Single File

This creates a single executable file. **Easier to distribute** but slower to start.

```bash
python build_onefile.py
```

**Output:** `dist/AutomationStudio.exe`

**Advantages:**
- Single file to distribute
- Simpler for end users
- No folder structure needed

**Disadvantages:**
- Slower startup (extracts to temp on each launch)
- Larger file size
- Example files embedded (harder to access)

---

## Build Process

### Step 1: Clean Previous Builds (Optional)

```bash
python clean_build.py
```

This removes all build artifacts from previous builds.

### Step 2: Run Build Script

Choose your build method:

```bash
# For folder-based distribution
python build.py

# OR for single-file distribution
python build_onefile.py
```

### Step 3: Test the Executable

Navigate to the `dist` folder and run the executable:

```bash
# For folder build
.\dist\AutomationStudio\AutomationStudio.exe

# For single file build
.\dist\AutomationStudio.exe
```

---

## Customization

### Adding an Icon

1. Create or obtain an `.ico` file (e.g., `icon.ico`)
2. Place it in the project root
3. Edit `automation-studio.spec`:
   ```python
   icon='icon.ico',  # Replace None with your icon path
   ```
4. Run `python build.py`

### Adjusting Build Settings

Edit `automation-studio.spec` to customize:

- **Console visibility:**
  ```python
  console=False,  # False = windowed app, True = shows console
  ```

- **Compression:**
  ```python
  upx=True,  # True = compress, False = no compression (faster build)
  ```

- **Additional files:**
  ```python
  datas=[
      ('examples', 'examples'),
      ('your_folder', 'your_folder'),  # Add more folders
  ],
  ```

- **Hidden imports** (if modules don't load):
  ```python
  hiddenimports=[
      'your_module',  # Add modules that fail to load
  ],
  ```

---

## Distribution

### Folder Build Distribution

Distribute the **entire** `dist/AutomationStudio` folder:

1. Zip the folder: `AutomationStudio.zip`
2. Users extract and run `AutomationStudio.exe`

### Single File Distribution

Distribute just the `dist/AutomationStudio.exe` file:

1. Users download and run directly
2. First launch may be slow (extracting to temp)

---

## Troubleshooting

### Build Fails

**Issue:** PyInstaller not found
```
✗ PyInstaller not found
```

**Solution:** Install PyInstaller
```bash
pip install pyinstaller
```

---

**Issue:** Module not found at runtime
```
ModuleNotFoundError: No module named 'xyz'
```

**Solution:** Add to hidden imports in `automation-studio.spec`:
```python
hiddenimports=[
    'xyz',  # Add the missing module
],
```

---

**Issue:** Missing data files
```
FileNotFoundError: [Errno 2] No such file or directory: 'examples/...'
```

**Solution:** Add to datas in `automation-studio.spec`:
```python
datas=[
    ('examples', 'examples'),
    ('your_data_folder', 'your_data_folder'),
],
```

---

### Executable Issues

**Issue:** Antivirus flags the executable

**Solution:** This is common with PyInstaller executables. Options:
1. Add exclusion in antivirus software
2. Code sign the executable (requires certificate)
3. Submit to antivirus vendor as false positive

---

**Issue:** Slow startup (single file build)

**Solution:** 
- This is normal for `--onefile` mode
- Use folder build (`build.py`) for faster startup
- Or accept the tradeoff for easier distribution

---

**Issue:** Large file size

**Solution:**
1. Enable UPX compression in spec file:
   ```python
   upx=True,
   ```
2. Exclude unnecessary modules:
   ```python
   excludes=[
       'matplotlib',
       'numpy',
       # Add more modules you don't use
   ],
   ```

---

## Advanced: Creating an Installer

For professional distribution, create an installer using:

### Inno Setup (Free)
1. Download: https://jrsoftware.org/isinfo.php
2. Create `.iss` script file
3. Compile to create installer

### NSIS (Free)
1. Download: https://nsis.sourceforge.io/
2. Create `.nsi` script file
3. Compile to create installer

### InstallForge (Free, GUI-based)
1. Download: https://installforge.net/
2. Use GUI to configure
3. Build installer

---

## Build Script Reference

### `build.py`
- Builds folder-based distribution
- Uses `automation-studio.spec` configuration
- Recommended for most users

### `build_onefile.py`
- Builds single-file executable
- Inline PyInstaller configuration
- Easier distribution, slower startup

### `clean_build.py`
- Removes all build artifacts
- Cleans `build/`, `dist/`, `__pycache__/`
- Run before fresh build

### `automation-studio.spec`
- PyInstaller configuration file
- Used by `build.py`
- Customize build settings here

---

## File Size Expectations

- **Folder build:** 80-120 MB (distributed)
- **Single file build:** 40-60 MB (single file)
- **With optimizations:** Can reduce by 20-30%

---

## Support

For build issues:
1. Check PyInstaller documentation: https://pyinstaller.org/
2. Review error messages carefully
3. Check `build/` folder for detailed logs
4. Try `--debug all` flag for verbose output

---

## Quick Reference

```bash
# Install dependencies
pip install -r requirements.txt

# Clean previous builds
python clean_build.py

# Build as folder (recommended)
python build.py

# Build as single file
python build_onefile.py

# Test executable
.\dist\AutomationStudio\AutomationStudio.exe
```

---

**Happy Building! 🚀**

