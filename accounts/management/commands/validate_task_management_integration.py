"""
Management command to validate task management module integration.
"""

from django.core.management.base import BaseCommand
from django.core.exceptions import ImproperlyConfigured
from task_management.integration import check_prerequisites, validate_integration


class Command(BaseCommand):
    help = 'Validate task management module integration configuration'

    def add_arguments(self, parser):
        parser.add_argument(
            '--fix',
            action='store_true',
            help='Attempt to fix common configuration issues',
        )
        parser.add_argument(
            '--verbose',
            action='store_true',
            help='Show detailed validation information',
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Validating task management module integration...'))
        
        try:
            # Check prerequisites
            errors = check_prerequisites()
            
            if errors:
                self.stdout.write(self.style.ERROR('❌ Prerequisites check failed:'))
                for error in errors:
                    self.stdout.write(self.style.ERROR(f'  - {error}'))
                
                if options['fix']:
                    self.stdout.write(self.style.WARNING('Attempting to fix issues...'))
                    self.fix_common_issues(errors)
                else:
                    self.stdout.write(self.style.WARNING('Run with --fix to attempt automatic fixes'))
                    return
            else:
                self.stdout.write(self.style.SUCCESS('✅ All prerequisites met'))
            
            # Validate integration
            validate_integration()
            self.stdout.write(self.style.SUCCESS('✅ Integration configuration is valid'))
            
            if options['verbose']:
                self.show_detailed_info()
            
            self.stdout.write(self.style.SUCCESS('\n🎉 Task management module is ready to use!'))
            
        except ImproperlyConfigured as e:
            self.stdout.write(self.style.ERROR(f'❌ Integration validation failed: {e}'))
            self.stdout.write(self.style.WARNING('Please fix the configuration issues above'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Unexpected error: {e}'))
    
    def fix_common_issues(self, errors):
        """Attempt to fix common configuration issues."""
        from django.conf import settings
        
        fixed_issues = []
        
        for error in errors:
            if "must be in INSTALLED_APPS" in error:
                app_name = error.split("'")[1]
                if hasattr(settings, 'INSTALLED_APPS'):
                    settings.INSTALLED_APPS = list(settings.INSTALLED_APPS) + [app_name]
                    fixed_issues.append(f"Added {app_name} to INSTALLED_APPS")
            
            elif "AUTH_USER_MODEL must be set" in error:
                if not hasattr(settings, 'AUTH_USER_MODEL'):
                    settings.AUTH_USER_MODEL = 'accounts.User'
                    fixed_issues.append("Set AUTH_USER_MODEL to 'accounts.User'")
            
            elif "LOGIN_URL should be set" in error:
                if not hasattr(settings, 'LOGIN_URL'):
                    settings.LOGIN_URL = 'task_management:login'
                    settings.LOGIN_REDIRECT_URL = 'task_management:dashboard'
                    settings.LOGOUT_REDIRECT_URL = 'task_management:login'
                    fixed_issues.append("Set login/logout URLs")
        
        if fixed_issues:
            self.stdout.write(self.style.SUCCESS('Fixed issues:'))
            for issue in fixed_issues:
                self.stdout.write(self.style.SUCCESS(f'  ✅ {issue}'))
        else:
            self.stdout.write(self.style.WARNING('No automatic fixes available for the detected issues'))
    
    def show_detailed_info(self):
        """Show detailed integration information."""
        from task_management.integration import get_integration_settings
        from django.conf import settings
        
        integration_settings = get_integration_settings()
        
        self.stdout.write(self.style.SUCCESS('\n📋 Integration Configuration:'))
        
        # Accounts settings
        self.stdout.write(self.style.SUCCESS('\nAccounts Configuration:'))
        accounts_config = integration_settings['accounts']
        for key, value in accounts_config.items():
            self.stdout.write(f"  {key}: {value}")
        
        # Tasks settings
        self.stdout.write(self.style.SUCCESS('\nTasks Configuration:'))
        tasks_config = integration_settings['tasks']
        for key, value in tasks_config.items():
            self.stdout.write(f"  {key}: {value}")
        
        # URL settings
        self.stdout.write(self.style.SUCCESS('\nURL Configuration:'))
        url_config = integration_settings['urls']
        for key, value in url_config.items():
            self.stdout.write(f"  {key}: {value}")
        
        # Database models
        self.stdout.write(self.style.SUCCESS('\n📊 Database Models:'))
        try:
            from accounts.models import User, Department
            from tasks.models import Task
            
            user_count = User.objects.count()
            dept_count = Department.objects.count()
            task_count = Task.objects.count()
            
            self.stdout.write(f"  Users: {user_count}")
            self.stdout.write(f"  Departments: {dept_count}")
            self.stdout.write(f"  Tasks: {task_count}")
        except Exception as e:
            self.stdout.write(self.style.WARNING(f"  Could not fetch database stats: {e}"))
        
        # URL patterns
        self.stdout.write(self.style.SUCCESS('\n🔗 Available URL Patterns:'))
        from django.urls import reverse
        from task_management.integration import get_url_namespace
        
        namespace = get_url_namespace()
        
        common_urls = [
            'dashboard',
            'login',
            'logout',
            'profile',
            'task-list',
            'task-create',
        ]
        
        for url_name in common_urls:
            try:
                if namespace:
                    url = reverse(f'{namespace}:{url_name}')
                else:
                    url = reverse(url_name)
                self.stdout.write(f"  {url_name}: {url}")
            except Exception as e:
                self.stdout.write(self.style.WARNING(f"  {url_name}: Not available - {e}"))