"""
Clean Build Script for Automation Studio
Removes all build artifacts and cache files
"""

import shutil
from pathlib import Path


def clean_build_artifacts():
    """Remove all build-related files and directories."""
    print("="*50)
    print("   Automation Studio - Clean Build")
    print("="*50)
    print()
    
    artifacts = [
        'build',
        'dist',
        '__pycache__',
        'src/__pycache__',
        'src/lib/__pycache__',
        'src/ui/__pycache__',
        '*.spec',
    ]
    
    print("Cleaning build artifacts...\n")
    
    removed_count = 0
    
    for artifact in artifacts:
        if '*' in artifact:
            # Handle glob patterns
            pattern = artifact
            for path in Path('.').rglob(pattern.replace('*', '')):
                if path.exists():
                    print(f"Removing: {path}")
                    if path.is_dir():
                        shutil.rmtree(path, ignore_errors=True)
                    else:
                        path.unlink()
                    removed_count += 1
        else:
            artifact_path = Path(artifact)
            if artifact_path.exists():
                print(f"Removing: {artifact_path}/")
                if artifact_path.is_dir():
                    shutil.rmtree(artifact_path, ignore_errors=True)
                else:
                    artifact_path.unlink()
                removed_count += 1
    
    # Clean all __pycache__ directories recursively
    print("\nCleaning all __pycache__ directories...")
    for pycache in Path('.').rglob('__pycache__'):
        if pycache.exists() and pycache.is_dir():
            print(f"Removing: {pycache}")
            shutil.rmtree(pycache, ignore_errors=True)
            removed_count += 1
    
    # Clean .pyc files
    print("\nCleaning .pyc files...")
    for pyc_file in Path('.').rglob('*.pyc'):
        if pyc_file.exists():
            print(f"Removing: {pyc_file}")
            pyc_file.unlink()
            removed_count += 1
    
    print("\n" + "="*50)
    if removed_count > 0:
        print(f"✓ Cleanup complete! Removed {removed_count} items")
    else:
        print("✓ Already clean - no artifacts found")
    print("="*50)


if __name__ == '__main__':
    clean_build_artifacts()

