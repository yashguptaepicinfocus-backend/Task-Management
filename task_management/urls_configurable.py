"""
Configurable URL configuration for the task management module.
This allows the module to be included with custom URL prefixes and namespaces.
"""

from django.urls import path, include
from django.conf import settings

# Get URL configuration from settings
def get_task_management_urls():
    """Get URL patterns for task management module."""
    
    # Import views here to avoid circular imports
    from accounts import urls as accounts_urls
    from tasks import urls as tasks_urls
    
    # Get namespace from settings or use default
    namespace = getattr(settings, 'TASK_MANAGEMENT_URL_NAMESPACE', 'task_management')
    
    # Base URL patterns
    urlpatterns = [
        path('', include(accounts_urls)),
        path('tasks/', include(tasks_urls)),
    ]
    
    return urlpatterns

def get_namespaced_urls():
    """Get URL patterns with namespace if configured."""
    urlpatterns = get_task_management_urls()
    
    # Check if namespace is enabled
    use_namespace = getattr(settings, 'TASK_MANAGEMENT_USE_NAMESPACE', True)
    namespace = getattr(settings, 'TASK_MANAGEMENT_URL_NAMESPACE', 'task_management')
    
    if use_namespace:
        return [path('', include((urlpatterns, namespace), namespace=namespace))]
    else:
        return urlpatterns