#!/usr/bin/env python3
"""
Manual PyPI Publishing Script
Use this if GitHub Actions trusted publishing fails
"""

import subprocess
import sys
import os
from pathlib import Path

def run_command(command, check=True):
    """Run a shell command and return the result."""
    print(f"Running: {command}")
    try:
        result = subprocess.run(command, shell=True, check=check, capture_output=True, text=True)
        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print(f"Warning: {result.stderr}")
        return result
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {e}")
        if e.stdout:
            print(f"Stdout: {e.stdout}")
        if e.stderr:
            print(f"Stderr: {e.stderr}")
        sys.exit(1)

def main():
    print("🚀 Manual PyPI Publishing Script")
    print("=" * 50)
    
    # Check if build and twine are installed
    print("📦 Checking dependencies...")
    try:
        import build
        import twine
    except ImportError:
        print("Installing build and twine...")
        run_command("pip install build twine")
    
    # Clean previous builds
    print("🧹 Cleaning previous builds...")
    dist_dir = Path("dist")
    if dist_dir.exists():
        import shutil
        shutil.rmtree(dist_dir)
    
    # Build package
    print("🔨 Building package...")
    run_command("python -m build")
    
    # Check package
    print("🔍 Checking package...")
    result = run_command("twine check dist/*", check=False)
    if result.returncode != 0:
        print("❌ Package check failed!")
        response = input("Continue anyway? (y/n): ")
        if response.lower() != 'y':
            sys.exit(1)
    
    print("\n📤 Ready to publish to PyPI!")
    print("\nChoose an option:")
    print("1. Publish to Test PyPI (recommended first)")
    print("2. Publish to Production PyPI")
    print("3. Just build, don't publish")
    
    choice = input("\nEnter your choice (1-3): ").strip()
    
    if choice == '1':
        print("\n📤 Publishing to Test PyPI...")
        run_command("twine upload --repository testpypi dist/*")
        print("\n✅ Published to Test PyPI!")
        print("Test installation:")
        print("pip install --index-url https://test.pypi.org/simple/ django-task-management")
        
    elif choice == '2':
        print("\n⚠️  Publishing to PRODUCTION PyPI!")
        response = input("Are you sure? Type 'yes' to confirm: ")
        if response.lower() == 'yes':
            run_command("twine upload dist/*")
            print("\n✅ Published to PyPI!")
            print("Installation:")
            print("pip install django-task-management")
        else:
            print("Publishing cancelled.")
            
    elif choice == '3':
        print("\n✅ Package built successfully!")
        print("Files created in dist/:")
        for file in Path("dist").glob("*"):
            print(f"  - {file.name}")
            
    else:
        print("Invalid choice. Exiting.")
        sys.exit(1)

if __name__ == "__main__":
    main()