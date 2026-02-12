# Django Task Management Module

A comprehensive, reusable Django module for task management with role-based access control, department hierarchy, and customizable workflows.

## Features

### Core Functionality
- **Task Management**: Create, assign, track, and manage tasks with status and priority
- **Role-Based Access Control**: Admin, Manager, and Employee roles with granular permissions
- **Department Hierarchy**: Organize users and tasks by departments
- **Task Comments**: Collaborative commenting system (configurable)
- **Status Tracking**: Customizable task status workflows
- **Priority Management**: Configurable priority levels
- **Due Date Tracking**: Automatic overdue detection
- **Dashboard**: Role-based dashboard with statistics

### Integration Features
- **Reusable Module**: Install as a Django package or copy module files
- **Configurable Settings**: Extensive customization through Django settings
- **Custom User Model**: Optional custom user model with role support
- **Template Override**: Override default templates with your own
- **URL Namespacing**: Configurable URL patterns with namespace support
- **Integration Validation**: Built-in validation for proper integration

## Quick Start

### Installation

```bash
pip install django-task-management
```

Or copy the `accounts/`, `tasks/`, and `task_management/` directories to your project.

### Basic Integration

1. **Add to INSTALLED_APPS**:
```python
# settings.py
INSTALLED_APPS = [
    # ... your existing apps
    'accounts',
    'tasks',
]
```

2. **Configure Authentication** (optional):
```python
AUTH_USER_MODEL = 'accounts.User'
LOGIN_URL = 'task_management:login'
LOGIN_REDIRECT_URL = 'task_management:dashboard'
LOGOUT_REDIRECT_URL = 'task_management:login'
```

3. **Include URLs**:
```python
# urls.py
urlpatterns = [
    # ... your existing URLs
    path('tasks/', include('task_management.urls')),
]
```

4. **Run Migrations**:
```bash
python manage.py makemigrations
python manage.py migrate
```

5. **Validate Integration**:
```bash
python manage.py validate_task_management_integration
```

## Configuration

### Custom Settings

```python
# settings.py

# Accounts configuration
TASK_MANAGEMENT_ACCOUNTS = {
    'ROLE_CHOICES': [
        ('admin', 'Administrator'),
        ('manager', 'Department Manager'),
        ('employee', 'Team Member'),
    ],
    'DEFAULT_ROLE': 'employee',
    'ALLOW_CROSS_DEPARTMENT_ASSIGNMENT': False,
}

# Tasks configuration
TASK_MANAGEMENT_TASKS = {
    'STATUS_CHOICES': [
        ('draft', 'Draft'),
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    ],
    'PRIORITY_CHOICES': [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ],
    'ALLOW_COMMENTS': True,
    'AUTO_COMPLETE_ON_STATUS_CHANGE': True,
}

# URL configuration
TASK_MANAGEMENT_URL_NAMESPACE = 'task_management'
TASK_MANAGEMENT_USE_NAMESPACE = True
```

### Custom Templates

Create your own templates to override defaults:

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

Set custom template base in settings:

```python
TASK_MANAGEMENT_ACCOUNTS = {
    'ACCOUNT_TEMPLATE_BASE': 'myapp/base.html',
}

TASK_MANAGEMENT_TASKS = {
    'TASK_TEMPLATE_BASE': 'myapp/base.html',
}
```

## Usage

### Creating Users and Departments

```python
from accounts.models import Department, User

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
```

### Creating Tasks

```python
from tasks.models import Task
from django.utils import timezone
from datetime import timedelta

# Create task
task = Task.objects.create(
    title="Implement new feature",
    description="Add user authentication to the application",
    created_by=manager,
    assigned_to=employee,
    department=dept,
    priority="high",
    due_date=timezone.now() + timedelta(days=7)
)
```

### Role-Based Permissions

```python
# Check user role
user.is_admin      # True for administrators
user.is_manager    # True for department managers
user.is_employee   # True for regular employees

# Check permissions
user.can_assign_tasks()           # Can assign tasks to others
user.can_assign_to_user(other_user)  # Can assign to specific user

# Get managed users
managed_users = user.get_managed_users()  # Users this user can assign tasks to
```

### Task Queries

```python
# Get tasks for user
user_tasks = Task.get_user_tasks(user)  # Tasks visible to user

# Get department tasks
dept_tasks = Task.get_department_tasks(department)

# Check task status
task.is_overdue        # True if past due date and not completed
task.days_remaining    # Days until due date
```

## URL Patterns

### Authentication URLs
- `/login/` - User login
- `/logout/` - User logout
- `/profile/` - User profile
- `/` - Dashboard (role-based)

### Task URLs
- `/tasks/` - Task list with filters
- `/tasks/my-tasks/` - Employee's assigned tasks
- `/tasks/create/` - Create new task
- `/tasks/<id>/` - Task detail view
- `/tasks/<id>/update/` - Update task
- `/tasks/<id>/delete/` - Delete task
- `/tasks/<id>/status/` - Update task status

## Integration with Existing Projects

### Using Existing User Model

```python
TASK_MANAGEMENT_ACCOUNTS = {
    'USE_CUSTOM_USER_MODEL': False,
    'USER_MODEL_NAME': 'auth.User',  # or your custom user model
}
```

### Custom Department Model

```python
TASK_MANAGEMENT_ACCOUNTS = {
    'DEPARTMENT_MODEL_NAME': 'myapp.Organization',
}
```

### Disable Features

```python
TASK_MANAGEMENT_TASKS = {
    'ALLOW_COMMENTS': False,  # Disable comments
    'REQUIRE_ASSIGNEE': True,  # Require assignee
    'AUTO_COMPLETE_ON_STATUS_CHANGE': False,  # Manual completion
}
```

## Management Commands

### Validate Integration

```bash
python manage.py validate_task_management_integration
```

Options:
- `--fix` - Attempt to fix common configuration issues
- `--verbose` - Show detailed validation information

### Create Sample Data

```python
# In Django shell
from accounts.models import Department, User
from tasks.models import Task

# Create sample departments and users
# ... your sample data creation code
```

## Testing

### Run Tests

```bash
python manage.py test accounts tasks
```

### Test Configuration

```python
# In your test settings
TASK_MANAGEMENT_ACCOUNTS = {
    'USE_CUSTOM_USER_MODEL': True,
    'ROLE_CHOICES': [
        ('admin', 'Admin'),
        ('manager', 'Manager'),
        ('employee', 'Employee'),
    ],
}

TASK_MANAGEMENT_TASKS = {
    'ALLOW_COMMENTS': True,
    'AUTO_COMPLETE_ON_STATUS_CHANGE': True,
}
```

## Deployment

### Production Settings

```python
# Disable debug mode
DEBUG = False

# Set allowed hosts
ALLOWED_HOSTS = ['yourdomain.com']

# Configure static files
STATIC_ROOT = BASE_DIR / 'staticfiles'
python manage.py collectstatic

# Set up email for notifications
TASK_MANAGEMENT_TASKS = {
    'SEND_NOTIFICATIONS': True,
}

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.your-provider.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'noreply@yourdomain.com'
EMAIL_HOST_PASSWORD = 'your-password'
```

### Database Configuration

```python
# PostgreSQL (recommended)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'task_management',
        'USER': 'postgres',
        'PASSWORD': 'your-password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

## Troubleshooting

### Common Issues

1. **Migration conflicts**: Handle existing user models carefully
2. **URL conflicts**: Ensure namespace doesn't conflict
3. **Template conflicts**: Use unique template names
4. **Permission issues**: Check role-based permissions

### Debug Mode

```python
# Enable detailed logging
LOGGING = {
    'loggers': {
        'accounts': {
            'level': 'DEBUG',
        },
        'tasks': {
            'level': 'DEBUG',
        },
    },
}
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support and questions:
1. Check the integration guide: `INTEGRATION_GUIDE.md`
2. Run validation: `python manage.py validate_task_management_integration --verbose`
3. Check the troubleshooting section
4. Create an issue on the repository

## Changelog

### Version 1.0.0
- Initial release
- Role-based access control
- Department hierarchy
- Configurable settings
- Template override support
- Integration validation
- Management commands