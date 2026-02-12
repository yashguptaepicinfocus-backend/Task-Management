"""
Integration helpers for the task management module.
This module provides utilities for integrating the task management system
into existing Django projects.
"""

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured


def check_prerequisites():
    """
    Check if all prerequisites for the task management module are met.
    
    Returns:
        list: List of error messages if any prerequisites are missing
    """
    errors = []
    
    # Check required apps
    required_apps = [
        'accounts',
        'tasks',
    ]
    
    for app in required_apps:
        if app not in settings.INSTALLED_APPS:
            errors.append(f"'{app}' must be in INSTALLED_APPS")
    
    # Check custom user model if enabled
    accounts_settings = getattr(settings, 'TASK_MANAGEMENT_ACCOUNTS', {})
    if accounts_settings.get('USE_CUSTOM_USER_MODEL', True):
        auth_user_model = getattr(settings, 'AUTH_USER_MODEL', None)
        expected_model = accounts_settings.get('USER_MODEL_NAME', 'accounts.User')
        
        if auth_user_model != expected_model:
            errors.append(f"AUTH_USER_MODEL must be set to '{expected_model}' when USE_CUSTOM_USER_MODEL is True")
    
    # Check login URLs
    login_url = getattr(settings, 'LOGIN_URL', None)
    expected_login_url = accounts_settings.get('LOGIN_URL', 'task_management:login')
    
    if login_url and login_url != expected_login_url:
        errors.append(f"LOGIN_URL should be set to '{expected_login_url}' for consistency")
    
    return errors


def get_integration_settings():
    """
    Get all integration settings for the task management module.
    
    Returns:
        dict: Dictionary containing all integration settings
    """
    return {
        'accounts': getattr(settings, 'TASK_MANAGEMENT_ACCOUNTS', {}),
        'tasks': getattr(settings, 'TASK_MANAGEMENT_TASKS', {}),
        'urls': {
            'namespace': getattr(settings, 'TASK_MANAGEMENT_URL_NAMESPACE', 'task_management'),
            'use_namespace': getattr(settings, 'TASK_MANAGEMENT_USE_NAMESPACE', True),
        }
    }


def validate_integration():
    """
    Validate that the task management module is properly configured.
    
    Raises:
        ImproperlyConfigured: If any configuration issues are found
    """
    errors = check_prerequisites()
    
    if errors:
        raise ImproperlyConfigured(
            "Task management module configuration errors:\n" + 
            "\n".join(f"- {error}" for error in errors)
        )


def get_url_namespace():
    """
    Get the URL namespace for the task management module.
    
    Returns:
        str: The URL namespace to use for reversing URLs
    """
    if getattr(settings, 'TASK_MANAGEMENT_USE_NAMESPACE', True):
        return getattr(settings, 'TASK_MANAGEMENT_URL_NAMESPACE', 'task_management')
    return None


def reverse_task_url(url_name, args=None, kwargs=None):
    """
    Reverse a task management URL with proper namespace.
    
    Args:
        url_name (str): The URL name to reverse
        args (list, optional): Positional arguments for URL reversal
        kwargs (dict, optional): Keyword arguments for URL reversal
    
    Returns:
        str: The reversed URL
    """
    from django.urls import reverse
    
    namespace = get_url_namespace()
    full_url_name = f"{namespace}:{url_name}" if namespace else url_name
    
    return reverse(full_url_name, args=args, kwargs=kwargs)