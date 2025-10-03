"""
Build Script for Automation Studio
Builds the application into a standalone executable using PyInstaller
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
    
    # Remove .spec file cache
    spec_file = Path('automation-studio.spec')
    if spec_file.exists():
        print(f"Found spec file: {spec_file}")
    
    print("✓ Cleanup complete\n")


def build_executable():
    """Build the executable using PyInstaller."""
    print("=== Building Executable ===")
    print("This may take a few minutes...\n")
    
    spec_file = 'automation-studio.spec'
    
    # Build command
    cmd = [
        sys.executable,
        '-m',
        'PyInstaller',
        spec_file,
        '--clean',
        '--noconfirm',
    ]
    
    print(f"Running: {' '.join(cmd)}\n")
    
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
    app_dir = dist_dir / 'AutomationStudio'
    exe_file = app_dir / 'AutomationStudio.exe'
    
    if exe_file.exists():
        print("\n✓ Executable built successfully!")
        print(f"\nLocation: {exe_file.absolute()}")
        print(f"Size: {exe_file.stat().st_size / (1024*1024):.2f} MB")
        
        print("\n" + "-"*50)
        print("Distribution folder contents:")
        print("-"*50)
        
        if app_dir.exists():
            files = list(app_dir.iterdir())
            print(f"\nTotal files: {len(files)}")
            print("\nMain files:")
            for file in sorted(files)[:10]:
                if file.is_file():
                    size_mb = file.stat().st_size / (1024*1024)
                    print(f"  • {file.name} ({size_mb:.2f} MB)")
            
            if len(files) > 10:
                print(f"  ... and {len(files) - 10} more files")
        
        print("\n" + "-"*50)
        print("Next Steps:")
        print("-"*50)
        print("1. Test the executable:")
        print(f"   {exe_file}")
        print("\n2. Distribute the entire folder:")
        print(f"   {app_dir}")
        print("\n3. Optional: Create installer using Inno Setup or NSIS")
        
    else:
        print("\n✗ Build completed but executable not found")
        print("Check the build output for errors")


def main():
    """Main build process."""
    print("="*50)
    print("   Automation Studio - Build Script")
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

