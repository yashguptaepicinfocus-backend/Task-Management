from django.apps import AppConfig
from django.conf import settings


class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'
    verbose_name = 'Task Management Accounts'
    
    def ready(self):
        """Initialize app settings when Django starts."""
        # Import settings module to ensure defaults are set
        from . import settings as app_settings
        
        # Set default settings if not already configured
        if not hasattr(settings, 'TASK_MANAGEMENT_ACCOUNTS'):
            settings.TASK_MANAGEMENT_ACCOUNTS = {}
        
        # Merge with defaults
        defaults = {
            'USE_CUSTOM_USER_MODEL': True,
            'USER_MODEL_NAME': 'accounts.User',
            'DEPARTMENT_MODEL_NAME': 'accounts.Department',
            'ROLE_CHOICES': [
                ('admin', 'Admin'),
                ('manager', 'Manager'),
                ('employee', 'Employee'),
            ],
            'DEFAULT_ROLE': 'employee',
            'ALLOW_CROSS_DEPARTMENT_ASSIGNMENT': False,
            'REQUIRE_DEPARTMENT_FOR_MANAGERS': True,
        }
        
        # Update settings with defaults for missing keys
        for key, value in defaults.items():
            if key not in settings.TASK_MANAGEMENT_ACCOUNTS:
                settings.TASK_MANAGEMENT_ACCOUNTS[key] = value