from django.apps import AppConfig
from django.conf import settings


class TasksConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'tasks'
    verbose_name = 'Task Management'
    
    def ready(self):
        """Initialize app settings when Django starts."""
        # Import settings module to ensure defaults are set
        from . import settings as app_settings
        
        # Set default settings if not already configured
        if not hasattr(settings, 'TASK_MANAGEMENT_TASKS'):
            settings.TASK_MANAGEMENT_TASKS = {}
        
        # Merge with defaults
        defaults = {
            'STATUS_CHOICES': [
                ('pending', 'Pending'),
                ('in_progress', 'In Progress'),
                ('completed', 'Completed'),
            ],
            'PRIORITY_CHOICES': [
                ('low', 'Low'),
                ('medium', 'Medium'),
                ('high', 'High'),
                ('urgent', 'Urgent'),
            ],
            'DEFAULT_STATUS': 'pending',
            'DEFAULT_PRIORITY': 'medium',
            'ALLOW_COMMENTS': True,
            'REQUIRE_ASSIGNEE': False,
            'AUTO_COMPLETE_ON_STATUS_CHANGE': True,
            'SEND_NOTIFICATIONS': False,
        }
        
        # Update settings with defaults for missing keys
        for key, value in defaults.items():
            if key not in settings.TASK_MANAGEMENT_TASKS:
                settings.TASK_MANAGEMENT_TASKS[key] = value