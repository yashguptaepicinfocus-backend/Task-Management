"""
Example settings for integrating the Django Task Management module.
Copy and modify these settings according to your needs.
"""

# Basic Django settings (add to your existing settings.py)

# 1. Add the required apps to INSTALLED_APPS
INSTALLED_APPS = [
    # ... your existing apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Task management apps
    'accounts',
    'tasks',
]

# 2. Configure authentication (optional - only if using custom user model)
AUTH_USER_MODEL = 'accounts.User'
LOGIN_URL = 'task_management:login'
LOGIN_REDIRECT_URL = 'task_management:dashboard'
LOGOUT_REDIRECT_URL = 'task_management:login'

# 3. Task Management Module Configuration

# Accounts app configuration
TASK_MANAGEMENT_ACCOUNTS = {
    # User model settings
    'USE_CUSTOM_USER_MODEL': True,  # Set to False if you want to use Django's default User model
    'USER_MODEL_NAME': 'accounts.User',  # Change if you have a custom user model
    'DEPARTMENT_MODEL_NAME': 'accounts.Department',  # Change if you have a custom department model
    
    # Role configuration
    'ROLE_CHOICES': [
        ('admin', 'Administrator'),
        ('manager', 'Department Manager'),
        ('employee', 'Team Member'),
        ('viewer', 'Read-Only User'),
    ],
    'DEFAULT_ROLE': 'employee',
    
    # Permission settings
    'ALLOW_CROSS_DEPARTMENT_ASSIGNMENT': False,  # Allow managers to assign tasks across departments
    'REQUIRE_DEPARTMENT_FOR_MANAGERS': True,  # Require managers to belong to a department
    
    # Template configuration
    'ACCOUNT_TEMPLATE_BASE': 'base.html',  # Base template for account pages
    'ACCOUNT_TEMPLATE_DIR': 'accounts',  # Directory for account templates
    
    # URL configuration
    'LOGIN_URL': 'task_management:login',
    'LOGIN_REDIRECT_URL': 'task_management:dashboard',
    'LOGOUT_REDIRECT_URL': 'task_management:login',
}

# Tasks app configuration
TASK_MANAGEMENT_TASKS = {
    # Status configuration
    'STATUS_CHOICES': [
        ('draft', 'Draft'),
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('review', 'Under Review'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ],
    'DEFAULT_STATUS': 'pending',
    
    # Priority configuration
    'PRIORITY_CHOICES': [
        ('low', 'Low'),
        ('normal', 'Normal'),
        ('high', 'High'),
        ('critical', 'Critical'),
    ],
    'DEFAULT_PRIORITY': 'normal',
    
    # Feature flags
    'ALLOW_COMMENTS': True,  # Enable/disable task comments
    'REQUIRE_ASSIGNEE': False,  # Require tasks to have an assignee
    'AUTO_COMPLETE_ON_STATUS_CHANGE': True,  # Auto-update completion date
    'SEND_NOTIFICATIONS': False,  # Enable email notifications (requires additional setup)
    
    # Template configuration
    'TASK_TEMPLATE_BASE': 'base.html',  # Base template for task pages
    'TASK_TEMPLATE_DIR': 'tasks',  # Directory for task templates
    
    # URL configuration
    'TASK_URL_NAMESPACE': 'task_management',
    'TASK_LIST_URL_NAME': 'task-list',
    'TASK_DETAIL_URL_NAME': 'task-detail',
}

# URL configuration
TASK_MANAGEMENT_URL_NAMESPACE = 'task_management'  # URL namespace for the module
TASK_MANAGEMENT_USE_NAMESPACE = True  # Use URL namespaces

# 4. Template Configuration
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            # Add your custom template directories here
            BASE_DIR / 'templates',
            # The module will also look in app directories due to APP_DIRS=True
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                # Add custom context processors if needed
            ],
        },
    },
]

# 5. Static Files Configuration
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
    # Add module static files if needed
]
STATIC_ROOT = BASE_DIR / 'staticfiles'

# 6. Media Files Configuration (if using file uploads)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# 7. Email Configuration (for notifications)
if TASK_MANAGEMENT_TASKS.get('SEND_NOTIFICATIONS', False):
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST = 'smtp.your-email-provider.com'
    EMAIL_PORT = 587
    EMAIL_USE_TLS = True
    EMAIL_HOST_USER = 'your-email@example.com'
    EMAIL_HOST_PASSWORD = 'your-email-password'
    DEFAULT_FROM_EMAIL = 'noreply@yourdomain.com'

# 8. Logging Configuration (optional - for debugging)
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'accounts': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': True,
        },
        'tasks': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}

# 9. Security Settings
# Make sure these are properly configured for production
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# 10. Custom Integration Settings
# Add any custom settings specific to your integration here

# Example: Custom role permissions
CUSTOM_ROLE_PERMISSIONS = {
    'admin': ['view_all_tasks', 'create_tasks', 'assign_tasks', 'manage_users'],
    'manager': ['view_department_tasks', 'create_tasks', 'assign_tasks'],
    'employee': ['view_assigned_tasks', 'update_task_status'],
    'viewer': ['view_all_tasks'],
}

# Example: Custom task workflows
CUSTOM_TASK_WORKFLOWS = {
    'simple': ['pending', 'in_progress', 'completed'],
    'review': ['draft', 'pending', 'in_progress', 'review', 'completed'],
    'complex': ['draft', 'pending', 'in_progress', 'review', 'testing', 'completed'],
}

# 11. Integration Validation
# You can validate your integration settings
INTEGRATION_VALIDATION = {
    'CHECK_PREREQUISITES': True,
    'VALIDATE_SETTINGS': True,
    'CHECK_DATABASE_CONNECTION': True,
}