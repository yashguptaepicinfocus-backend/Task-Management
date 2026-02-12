# Publishing Your Django Task Management Module to PyPI

This guide will walk you through publishing your Django Task Management module to the Python Package Index (PyPI) so others can install it with `pip install django-task-management`.

## 📋 Prerequisites

1. **Python 3.8+** installed
2. **pip** and **setuptools** updated
3. **PyPI account** (create at https://pypi.org/account/register/)
4. **Git** repository (recommended)

## 🔧 Step 1: Prepare Your Package

### 1.1 Update Package Information

Edit these files with your information:

**`pyproject.toml`**:
```toml
[project]
name = "django-task-management"
version = "1.0.0"
authors = [
    {name = "YOUR_NAME", email = "YOUR_EMAIL@example.com"},
]
description = "A comprehensive Django task management module with role-based access control"
```

**`setup.py`** (if you prefer using setup.py instead of pyproject.toml):
```python
author="YOUR_NAME",
author_email="YOUR_EMAIL@example.com",
url="https://github.com/YOUR_USERNAME/django-task-management",
```

### 1.2 Clean Up Your Package

Remove unnecessary files:
```bash
# Remove Python cache
find . -type d -name "__pycache__" -exec rm -rf {} +
find . -name "*.pyc" -delete

# Remove database files (if any)
rm -f db.sqlite3

# Remove virtual environment (if in project)
rm -rf venv/
```

## 🏗️ Step 2: Build Your Package

### 2.1 Install Build Tools

```bash
pip install build twine
```

### 2.2 Build the Package

```bash
# Using pyproject.toml (recommended)
python -m build

# Or using setup.py directly
python setup.py sdist bdist_wheel
```

This creates files in the `dist/` directory:
- `django-task-management-1.0.0.tar.gz` (source distribution)
- `django_task_management-1.0.0-py3-none-any.whl` (wheel distribution)

## 🧪 Step 3: Test Your Package Locally

### 3.1 Install Locally

```bash
# Install the wheel file locally
pip install dist/django_task_management-1.0.0-py3-none-any.whl

# Or install in development mode
pip install -e .
```

### 3.2 Test in a New Django Project

```bash
# Create a test Django project
django-admin startproject test_project
cd test_project

# Add to settings.py
INSTALLED_APPS = [
    'accounts',
    'tasks',
    # ... other apps
]

# Include URLs
path('tasks/', include('task_management.urls')),

# Run migrations
python manage.py makemigrations
python manage.py migrate

# Test the module
python manage.py validate_task_management_integration
```

## 🔐 Step 4: Create PyPI Account

1. Go to https://pypi.org/account/register/
2. Create your account
3. **Enable 2FA** (Two-Factor Authentication) - **Required for new accounts**
4. Create an API token:
   - Go to Account Settings → API tokens
   - Click "Add API token"
   - Name it (e.g., "django-task-management")
   - Scope: "Entire account" (or "Project: django-task-management" if updating)
   - **Save the token securely** - you won't see it again!

## 📤 Step 5: Upload to PyPI

### 5.1 Configure Authentication

Create a `~/.pypirc` file:
```ini
[distutils]
index-servers =
    pypi
    testpypi

[pypi]
username = __token__
password = YOUR_API_TOKEN_HERE

[testpypi]
username = __token__
password = YOUR_TEST_API_TOKEN_HERE
```

### 5.2 Upload to Test PyPI (Recommended First)

```bash
# Upload to Test PyPI
python -m twine upload --repository testpypi dist/*

# Install from Test PyPI to test
pip install --index-url https://test.pypi.org/simple/ django-task-management
```

### 5.3 Upload to Production PyPI

```bash
# Upload to production PyPI
python -m twine upload dist/*
```

## ✅ Step 6: Verify Installation

### 6.1 Install from PyPI

```bash
# Install your package
pip install django-task-management

# Verify installation
pip show django-task-management
```

### 6.2 Test in a New Project

```bash
# Create a new Django project
django-admin startproject myproject
cd myproject

# Add to INSTALLED_APPS in settings.py
INSTALLED_APPS = [
    'accounts',
    'tasks',
    'django.contrib.admin',
    'django.contrib.auth',
    # ... other apps
]

# Run migrations
python manage.py migrate

# Test the module
python manage.py validate_task_management_integration
```

## 🔄 Step 7: Maintenance and Updates

### 7.1 Version Updates

1. Update version in `pyproject.toml` or `setup.py`
2. Update `CHANGELOG.md` with new features/fixes
3. Build and upload new version
4. Test the new version

### 7.2 GitHub Actions (Optional Automation)

Create `.github/workflows/publish.yml`:
```yaml
name: Publish to PyPI

on:
  release:
    types: [published]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.x'
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install build twine
    - name: Build package
      run: python -m build
    - name: Publish to PyPI
      env:
        TWINE_USERNAME: __token__
        TWINE_PASSWORD: ${{ secrets.PYPI_API_TOKEN }}
      run: twine upload dist/*
```

Add your PyPI API token as a GitHub secret: `PYPI_API_TOKEN`

## 📋 Checklist Before Publishing

- [ ] **Package Information**: Updated name, version, author, description
- [ ] **License**: Added appropriate license file
- [ ] **Documentation**: README and integration guides are complete
- [ ] **Testing**: Package installs and works correctly
- [ ] **Version**: Correct version number
- [ ] **Dependencies**: All dependencies are specified
- [ ] **Clean**: No unnecessary files (cache, database, etc.)
- [ ] **Build**: Package builds successfully
- [ ] **Test PyPI**: Tested on Test PyPI first (recommended)
- [ ] **API Token**: PyPI API token created and configured

## 🚨 Important Notes

### **Security**
- **Never commit API tokens** to your repository
- Use GitHub Secrets for CI/CD workflows
- Enable 2FA on your PyPI account

### **Naming**
- Package name should be unique on PyPI
- Check availability: https://pypi.org/search/?q=django-task-management
- Consider using your username prefix if name is taken

### **Versioning**
- Follow [Semantic Versioning](https://semver.org/):
  - MAJOR.MINOR.PATCH (e.g., 1.0.0)
  - MAJOR: Breaking changes
  - MINOR: New features (backward compatible)
  - PATCH: Bug fixes

### **Documentation**
- Good documentation increases adoption
- Include examples and use cases
- Keep README.md up to date

## 🎯 Alternative Publishing Options

### **Private PyPI Server**
For internal/company use:
```bash
# Install devpi-server
pip install devpi-server
devpi-server --start

# Upload to private server
twine upload --repository-url http://localhost:3141/root/pypi/ dist/*
```

### **GitHub Packages**
For GitHub-based distribution:
```bash
# Build and upload to GitHub Packages
twine upload --repository-url https://uploads.github.com/YOUR_USERNAME/django-task-management dist/*
```

### **Direct Installation from Git**
For development/testing:
```bash
pip install git+https://github.com/YOUR_USERNAME/django-task-management.git
```

## 📞 Support

If you encounter issues:
1. Check PyPI documentation: https://packaging.python.org/
2. PyPI help: https://pypi.org/help/
3. Python packaging guide: https://packaging.python.org/guides/

## 🎉 Congratulations!

Once published, your package will be available at:
**https://pypi.org/project/django-task-management/**

Users can then install it with:
```bash
pip install django-task-management
```

Happy publishing! 🚀