"""
Default settings for the tasks app.
These can be overridden in the main Django settings file.
"""

from django.conf import settings

# Get user-defined settings or use defaults
TASK_MANAGEMENT_TASKS = getattr(settings, 'TASK_MANAGEMENT_TASKS', {})

# Task configuration
STATUS_CHOICES = TASK_MANAGEMENT_TASKS.get('STATUS_CHOICES', [
    ('pending', 'Pending'),
    ('in_progress', 'In Progress'),
    ('completed', 'Completed'),
])
PRIORITY_CHOICES = TASK_MANAGEMENT_TASKS.get('PRIORITY_CHOICES', [
    ('low', 'Low'),
    ('medium', 'Medium'),
    ('high', 'High'),
    ('urgent', 'Urgent'),
])
DEFAULT_STATUS = TASK_MANAGEMENT_TASKS.get('DEFAULT_STATUS', 'pending')
DEFAULT_PRIORITY = TASK_MANAGEMENT_TASKS.get('DEFAULT_PRIORITY', 'medium')

# Feature flags
ALLOW_COMMENTS = TASK_MANAGEMENT_TASKS.get('ALLOW_COMMENTS', True)
REQUIRE_ASSIGNEE = TASK_MANAGEMENT_TASKS.get('REQUIRE_ASSIGNEE', False)
AUTO_COMPLETE_ON_STATUS_CHANGE = TASK_MANAGEMENT_TASKS.get('AUTO_COMPLETE_ON_STATUS_CHANGE', True)
SEND_NOTIFICATIONS = TASK_MANAGEMENT_TASKS.get('SEND_NOTIFICATIONS', False)

# Template configuration
TASK_TEMPLATE_BASE = TASK_MANAGEMENT_TASKS.get('TASK_TEMPLATE_BASE', 'base.html')
TASK_TEMPLATE_DIR = TASK_MANAGEMENT_TASKS.get('TASK_TEMPLATE_DIR', 'tasks')

# URL configuration
TASK_URL_NAMESPACE = TASK_MANAGEMENT_TASKS.get('TASK_URL_NAMESPACE', 'task_management')
TASK_LIST_URL_NAME = TASK_MANAGEMENT_TASKS.get('TASK_LIST_URL_NAME', 'task-list')
TASK_DETAIL_URL_NAME = TASK_MANAGEMENT_TASKS.get('TASK_DETAIL_URL_NAME', 'task-detail')