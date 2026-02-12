# Django Task Management Module - Integration Guide

This guide explains how to integrate the Django Task Management module into your existing Django project.

## Installation

### Option 1: Install as Package

```bash
pip install django-task-management
```

### Option 2: Copy Module Files

Copy the following directories and files to your project:
- `accounts/` - User management and authentication
- `tasks/` - Task management functionality
- `task_management/integration.py` - Integration utilities
- `task_management/urls_configurable.py` - URL configuration

## Basic Integration

### 1. Add Apps to INSTALLED_APPS

Add these apps to your `settings.py`:

```python
INSTALLED_APPS = [
    # ... your existing apps
    'accounts',
    'tasks',
]
```

### 2. Configure Authentication (Optional)

If you want to use the custom user model:

```python
# settings.py
AUTH_USER_MODEL = 'accounts.User'

# Login/logout URLs
LOGIN_URL = 'task_management:login'
LOGIN_REDIRECT_URL = 'task_management:dashboard'
LOGOUT_REDIRECT_URL = 'task_management:login'
```

### 3. Include URLs

In your main `urls.py`:

```python
from django.urls import path, include

urlpatterns = [
    # ... your existing URLs
    path('task-management/', include('task_management.urls')),
]
```

### 4. Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

## Advanced Configuration

### Custom Settings

You can customize the module behavior through settings:

```python
# settings.py

# Accounts app configuration
TASK_MANAGEMENT_ACCOUNTS = {
    'USE_CUSTOM_USER_MODEL': True,
    'ROLE_CHOICES': [
        ('admin', 'Administrator'),
        ('manager', 'Department Manager'),
        ('employee', 'Team Member'),
        ('viewer', 'Read-Only User'),
    ],
    'DEFAULT_ROLE': 'employee',
    'ALLOW_CROSS_DEPARTMENT_ASSIGNMENT': False,
    'REQUIRE_DEPARTMENT_FOR_MANAGERS': True,
}

# Tasks app configuration
TASK_MANAGEMENT_TASKS = {
    'STATUS_CHOICES': [
        ('draft', 'Draft'),
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('review', 'Under Review'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ],
    'PRIORITY_CHOICES': [
        ('low', 'Low'),
        ('normal', 'Normal'),
        ('high', 'High'),
        ('critical', 'Critical'),
    ],
    'DEFAULT_STATUS': 'draft',
    'DEFAULT_PRIORITY': 'normal',
    'ALLOW_COMMENTS': True,
    'REQUIRE_ASSIGNEE': False,
    'AUTO_COMPLETE_ON_STATUS_CHANGE': True,
    'SEND_NOTIFICATIONS': True,
}

# URL configuration
TASK_MANAGEMENT_URL_NAMESPACE = 'task_management'
TASK_MANAGEMENT_USE_NAMESPACE = True
```

### Custom Templates

You can override the default templates by creating your own:

```
your_project/
├── templates/
│   ├── accounts/
│   │   ├── login.html
│   │   ├── dashboard.html
│   │   └── profile.html
│   └── tasks/
│       ├── task_list.html
│       ├── task_detail.html
│       ├── task_form.html
│       └── task_confirm_delete.html
```

### Custom Styling

The module uses Bootstrap 5 by default. You can customize the styling by:

1. **Override base template**: Create your own `base.html` that the module templates extend
2. **Custom CSS**: Add your own CSS files and override the blocks in templates
3. **Custom template base**: Set custom template base in settings

```python
TASK_MANAGEMENT_ACCOUNTS = {
    'ACCOUNT_TEMPLATE_BASE': 'myapp/base.html',
}

TASK_MANAGEMENT_TASKS = {
    'TASK_TEMPLATE_BASE': 'myapp/base.html',
}
```

## Integration Examples

### Using with Existing User Model

If you want to use your existing user model instead of the custom one:

```python
# settings.py
TASK_MANAGEMENT_ACCOUNTS = {
    'USE_CUSTOM_USER_MODEL': False,
    'USER_MODEL_NAME': 'auth.User',  # or your custom user model
}
```

### Custom Department Model

If you have your own department/organization model:

```python
# settings.py
TASK_MANAGEMENT_ACCOUNTS = {
    'DEPARTMENT_MODEL_NAME': 'myapp.Organization',
}
```

### Disable Comments

To disable the task comment feature:

```python
# settings.py
TASK_MANAGEMENT_TASKS = {
    'ALLOW_COMMENTS': False,
}
```

### Custom URL Patterns

To use custom URL patterns without namespace:

```python
# settings.py
TASK_MANAGEMENT_USE_NAMESPACE = False

# urls.py
from task_management.integration import get_namespaced_urls

urlpatterns = [
    # ... your existing URLs
    path('tasks/', include(get_namespaced_urls())),
]
```

## Validation

You can validate your integration configuration:

```python
# In your Django shell or management command
from task_management.integration import validate_integration

try:
    validate_integration()
    print("Integration configuration is valid!")
except ImproperlyConfigured as e:
    print(f"Configuration error: {e}")
```

## Database Integration

### Using with Existing Database

If you have existing users and departments, you can map them:

```python
# In a data migration or management command
from django.apps import apps
from task_management.integration import get_integration_settings

settings = get_integration_settings()
User = apps.get_model(settings['accounts']['USER_MODEL_NAME'])
Department = apps.get_model(settings['accounts']['DEPARTMENT_MODEL_NAME'])

# Map existing data to task management structure
```

### Custom User Fields

If you need to add custom fields to the user model:

```python
# accounts/models.py (extend the existing User model)
from accounts.models import User as BaseUser

class User(BaseUser):
    # Add your custom fields
    custom_field = models.CharField(max_length=100)
    
    class Meta:
        proxy = True  # This extends the existing model without creating new table
```

## Testing Integration

### Create Test Data

```python
# In Django shell
from accounts.models import Department, User
from tasks.models import Task

# Create department
dept = Department.objects.create(name="IT", description="IT Department")

# Create users
admin = User.objects.create_user(
    username="admin",
    email="admin@example.com",
    password="password",
    role="admin",
    first_name="Admin",
    last_name="User"
)

manager = User.objects.create_user(
    username="manager",
    email="manager@example.com",
    password="password",
    role="manager",
    department=dept,
    first_name="Manager",
    last_name="User"
)

employee = User.objects.create_user(
    username="employee",
    email="employee@example.com",
    password="password",
    role="employee",
    department=dept,
    first_name="Employee",
    last_name="User"
)

# Create task
task = Task.objects.create(
    title="Test Task",
    description="This is a test task",
    created_by=manager,
    assigned_to=employee,
    department=dept,
    priority="high",
    due_date="2024-12-31"
)
```

### Test Permissions

```python
# Test role-based permissions
from django.test import TestCase
from django.contrib.auth import get_user_model

User = get_user_model()

class TaskManagementTest(TestCase):
    def test_admin_permissions(self):
        admin = User.objects.create_user(username="admin", role="admin")
        self.assertTrue(admin.is_admin)
        self.assertTrue(admin.can_assign_tasks())
    
    def test_manager_permissions(self):
        dept = Department.objects.create(name="IT")
        manager = User.objects.create_user(username="manager", role="manager", department=dept)
        self.assertTrue(manager.is_manager)
        self.assertTrue(manager.can_assign_tasks())
```

## Troubleshooting

### Common Issues

1. **Migration conflicts**: If you have existing user models, you may need to handle migrations carefully
2. **URL conflicts**: Ensure the URL namespace doesn't conflict with existing URLs
3. **Template conflicts**: Make sure template names don't conflict with existing templates
4. **Permission issues**: Check that role-based permissions are working as expected

### Debug Settings

```python
# settings.py
DEBUG = True

# Enable detailed logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'accounts': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
        'tasks': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    },
}
```

## Next Steps

1. **Customize templates** to match your application's design
2. **Add custom business logic** by extending views and models
3. **Integrate with existing workflows** in your application
4. **Add API endpoints** if needed for mobile or frontend applications
5. **Set up notifications** for task assignments and updates
6. **Add reporting features** for task analytics

For more advanced customization, refer to the module's source code and extend the classes as needed.