"""
Default settings for the accounts app.
These can be overridden in the main Django settings file.
"""

from django.conf import settings

# Get user-defined settings or use defaults
TASK_MANAGEMENT_ACCOUNTS = getattr(settings, 'TASK_MANAGEMENT_ACCOUNTS', {})

# User model configuration
USE_CUSTOM_USER_MODEL = TASK_MANAGEMENT_ACCOUNTS.get('USE_CUSTOM_USER_MODEL', True)
USER_MODEL_NAME = TASK_MANAGEMENT_ACCOUNTS.get('USER_MODEL_NAME', 'accounts.User')
DEPARTMENT_MODEL_NAME = TASK_MANAGEMENT_ACCOUNTS.get('DEPARTMENT_MODEL_NAME', 'accounts.Department')

# Role configuration
ROLE_CHOICES = TASK_MANAGEMENT_ACCOUNTS.get('ROLE_CHOICES', [
    ('admin', 'Admin'),
    ('manager', 'Manager'),
    ('employee', 'Employee'),
])
DEFAULT_ROLE = TASK_MANAGEMENT_ACCOUNTS.get('DEFAULT_ROLE', 'employee')

# Permission settings
ALLOW_CROSS_DEPARTMENT_ASSIGNMENT = TASK_MANAGEMENT_ACCOUNTS.get('ALLOW_CROSS_DEPARTMENT_ASSIGNMENT', False)
REQUIRE_DEPARTMENT_FOR_MANAGERS = TASK_MANAGEMENT_ACCOUNTS.get('REQUIRE_DEPARTMENT_FOR_MANAGERS', True)

# URL configuration
LOGIN_URL = TASK_MANAGEMENT_ACCOUNTS.get('LOGIN_URL', 'task_management:login')
LOGIN_REDIRECT_URL = TASK_MANAGEMENT_ACCOUNTS.get('LOGIN_REDIRECT_URL', 'task_management:dashboard')
LOGOUT_REDIRECT_URL = TASK_MANAGEMENT_ACCOUNTS.get('LOGOUT_REDIRECT_URL', 'task_management:login')

# Template configuration
ACCOUNT_TEMPLATE_BASE = TASK_MANAGEMENT_ACCOUNTS.get('ACCOUNT_TEMPLATE_BASE', 'base.html')
ACCOUNT_TEMPLATE_DIR = TASK_MANAGEMENT_ACCOUNTS.get('ACCOUNT_TEMPLATE_DIR', 'accounts')