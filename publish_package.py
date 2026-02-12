#!/usr/bin/env python3
"""
Automated script to build and publish the Django Task Management package to PyPI.

Usage:
    python publish_package.py --test     # Publish to Test PyPI
    python publish_package.py --prod     # Publish to PyPI
    python publish_package.py --build    # Just build the package
"""

import os
import sys
import subprocess
import shutil
import argparse
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


def clean_build_artifacts():
    """Clean up build artifacts."""
    print("🧹 Cleaning build artifacts...")
    
    dirs_to_clean = ['build', 'dist', '*.egg-info']
    for pattern in dirs_to_clean:
        for path in Path('.').glob(pattern):
            if path.is_dir():
                shutil.rmtree(path)
                print(f"Removed directory: {path}")
            elif path.is_file():
                path.unlink()
                print(f"Removed file: {path}")


def clean_python_cache():
    """Clean Python cache files."""
    print("🧹 Cleaning Python cache...")
    
    for root, dirs, files in os.walk('.'):
        for dir_name in dirs:
            if dir_name == '__pycache__':
                cache_dir = os.path.join(root, dir_name)
                shutil.rmtree(cache_dir)
                print(f"Removed cache directory: {cache_dir}")
        
        for file_name in files:
            if file_name.endswith('.pyc') or file_name.endswith('.pyo'):
                cache_file = os.path.join(root, file_name)
                os.remove(cache_file)
                print(f"Removed cache file: {cache_file}")


def validate_package():
    """Validate the package before building."""
    print("🔍 Validating package...")
    
    # Check for required files
    required_files = [
        'pyproject.toml',
        'MODULE_README.md',
        'LICENSE',
        'CHANGELOG.md',
        'accounts',
        'tasks',
        'task_management'
    ]
    
    missing_files = []
    for file_path in required_files:
        if not os.path.exists(file_path):
            missing_files.append(file_path)
    
    if missing_files:
        print(f"❌ Missing required files: {missing_files}")
        return False
    
    print("✅ All required files present")
    return True


def install_build_dependencies():
    """Install build dependencies."""
    print("📦 Installing build dependencies...")
    run_command("pip install --upgrade pip build twine")


def build_package():
    """Build the package."""
    print("🔨 Building package...")
    run_command("python -m build")
    
    # Check if build was successful
    dist_dir = Path('dist')
    if not dist_dir.exists():
        print("❌ Build failed - dist directory not created")
        return False
    
    wheel_files = list(dist_dir.glob('*.whl'))
    tar_files = list(dist_dir.glob('*.tar.gz'))
    
    if not wheel_files or not tar_files:
        print("❌ Build failed - expected files not found")
        return False
    
    print(f"✅ Build successful - created {len(wheel_files)} wheel and {len(tar_files)} source files")
    return True


def check_package():
    """Check the built package with twine."""
    print("🔍 Checking package with twine...")
    run_command("twine check dist/*")


def upload_to_testpypi():
    """Upload to Test PyPI."""
    print("📤 Uploading to Test PyPI...")
    run_command("twine upload --repository testpypi dist/*")


def upload_to_pypi():
    """Upload to PyPI."""
    print("📤 Uploading to PyPI...")
    run_command("twine upload dist/*")


def main():
    parser = argparse.ArgumentParser(description='Build and publish Django Task Management package')
    parser.add_argument('--test', action='store_true', help='Upload to Test PyPI')
    parser.add_argument('--prod', action='store_true', help='Upload to PyPI')
    parser.add_argument('--build', action='store_true', help='Just build the package')
    parser.add_argument('--clean', action='store_true', help='Clean build artifacts')
    parser.add_argument('--validate', action='store_true', help='Validate package only')
    parser.add_argument('--skip-clean', action='store_true', help='Skip cleaning build artifacts')
    
    args = parser.parse_args()
    
    print("🚀 Django Task Management Package Publisher")
    print("=" * 50)
    
    # Default action if no arguments provided
    if not any([args.test, args.prod, args.build, args.clean, args.validate]):
        print("No action specified. Use --help for options.")
        return
    
    # Clean build artifacts if requested
    if args.clean:
        clean_build_artifacts()
        return
    
    # Validate package
    if args.validate:
        validate_package()
        return
    
    # Clean Python cache
    clean_python_cache()
    
    # Validate package before building
    if not validate_package():
        print("❌ Package validation failed")
        return
    
    # Clean build artifacts unless skipped
    if not args.skip_clean:
        clean_build_artifacts()
    
    # Install build dependencies
    install_build_dependencies()
    
    # Build package
    if not build_package():
        print("❌ Build failed")
        return
    
    # Check package
    check_package()
    
    # Upload based on arguments
    if args.test:
        upload_to_testpypi()
        print("\n✅ Package uploaded to Test PyPI!")
        print("Test installation: pip install --index-url https://test.pypi.org/simple/ django-task-management")
    
    elif args.prod:
        # Confirm before uploading to production
        response = input("Are you sure you want to upload to PRODUCTION PyPI? (yes/no): ")
        if response.lower() == 'yes':
            upload_to_pypi()
            print("\n✅ Package uploaded to PyPI!")
            print("Install with: pip install django-task-management")
        else:
            print("Upload to PyPI cancelled")
    
    elif args.build:
        print("\n✅ Package built successfully!")
        print("Files created in dist/ directory")
    
    print("\n🎉 Process completed!")


if __name__ == "__main__":
    main()