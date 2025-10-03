"""
Build Script for Automation Studio (Single File Version)
Builds the application into a single executable file using PyInstaller
"""

import subprocess
import sys
import shutil
from pathlib import Path


def check_pyinstaller():
    """Check if PyInstaller is installed."""
    try:
        import PyInstaller
        print(f"✓ PyInstaller {PyInstaller.__version__} found")
        return True
    except ImportError:
        print("✗ PyInstaller not found")
        print("\nPlease install PyInstaller:")
        print("  pip install pyinstaller")
        return False


def clean_build_artifacts():
    """Remove previous build artifacts."""
    print("\n=== Cleaning Build Artifacts ===")
    
    artifacts = ['build', 'dist', '__pycache__']
    
    for artifact in artifacts:
        artifact_path = Path(artifact)
        if artifact_path.exists():
            print(f"Removing {artifact}/")
            shutil.rmtree(artifact_path, ignore_errors=True)
    
    print("✓ Cleanup complete\n")


def build_executable():
    """Build the executable using PyInstaller (one-file mode)."""
    print("=== Building Single File Executable ===")
    print("This may take several minutes...\n")
    print("Note: Single file executables are slower to start but easier to distribute\n")
    
    # Build command for one-file
    cmd = [
        sys.executable,
        '-m',
        'PyInstaller',
        '--onefile',
        '--windowed',
        '--name=AutomationStudio',
        '--clean',
        '--noconfirm',
        # Add data files
        '--add-data=examples;examples',
        '--add-data=automations;automations',
        # Hidden imports
        '--hidden-import=tkinter',
        '--hidden-import=tkinter.ttk',
        '--hidden-import=tkinter.scrolledtext',
        '--hidden-import=pyautogui',
        '--hidden-import=pyperclip',
        '--hidden-import=yaml',
        '--hidden-import=keyboard',
        '--hidden-import=PIL',
        '--hidden-import=PIL._tkinter_finder',
        # Exclude unnecessary modules
        '--exclude-module=matplotlib',
        '--exclude-module=numpy',
        '--exclude-module=pandas',
        '--exclude-module=scipy',
        '--exclude-module=pytest',
        '--exclude-module=setuptools',
        # Main file
        'app.py',
    ]
    
    print(f"Running PyInstaller...\n")
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=False)
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n✗ Build failed with error code {e.returncode}")
        return False
    except Exception as e:
        print(f"\n✗ Build failed: {str(e)}")
        return False


def display_results():
    """Display build results."""
    print("\n" + "="*50)
    print("=== Build Complete ===")
    print("="*50)
    
    dist_dir = Path('dist')
    exe_file = dist_dir / 'AutomationStudio.exe'
    
    if exe_file.exists():
        print("\n✓ Single file executable built successfully!")
        print(f"\nLocation: {exe_file.absolute()}")
        print(f"Size: {exe_file.stat().st_size / (1024*1024):.2f} MB")
        
        print("\n" + "-"*50)
        print("Next Steps:")
        print("-"*50)
        print("1. Test the executable:")
        print(f"   {exe_file}")
        print("\n2. Distribute the single file:")
        print(f"   {exe_file.name}")
        print("\n3. Note: First launch may be slower as it extracts files to temp")
        print("\nAdvantages of single file:")
        print("  • Easy to distribute (just one file)")
        print("  • No folder structure to maintain")
        print("\nDisadvantages:")
        print("  • Slower startup time")
        print("  • Larger file size")
        print("  • Example files are embedded (users can't easily access them)")
        
    else:
        print("\n✗ Build completed but executable not found")
        print("Check the build output for errors")


def main():
    """Main build process."""
    print("="*50)
    print("   Automation Studio - Single File Build")
    print("="*50)
    print()
    
    # Check dependencies
    if not check_pyinstaller():
        sys.exit(1)
    
    # Clean previous builds
    clean_build_artifacts()
    
    # Build executable
    if not build_executable():
        print("\n✗ Build failed")
        sys.exit(1)
    
    # Display results
    display_results()


if __name__ == '__main__':
    main()

