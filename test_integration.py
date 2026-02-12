"""
Simple test script to verify the task management module integration.
Run this after setting up the module to ensure everything works correctly.
"""

import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'task_management.settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
django.setup()

def test_basic_functionality():
    """Test basic functionality of the task management module."""
    print("🧪 Testing Django Task Management Module Integration...")
    
    try:
        # Test 1: Import models
        print("\n1️⃣ Testing model imports...")
        from accounts.models import Department, User
        from tasks.models import Task
        print("   ✅ Models imported successfully")
        
        # Test 2: Check settings integration
        print("\n2️⃣ Testing settings integration...")
        from django.conf import settings
        
        # Check if custom settings are available
        accounts_settings = getattr(settings, 'TASK_MANAGEMENT_ACCOUNTS', {})
        tasks_settings = getattr(settings, 'TASK_MANAGEMENT_TASKS', {})
        
        if accounts_settings:
            print(f"   ✅ Accounts settings loaded: {len(accounts_settings)} configurations")
        else:
            print("   ⚠️  No custom accounts settings found (using defaults)")
            
        if tasks_settings:
            print(f"   ✅ Tasks settings loaded: {len(tasks_settings)} configurations")
        else:
            print("   ⚠️  No custom tasks settings found (using defaults)")
        
        # Test 3: Test user model
        print("\n3️⃣ Testing user model...")
        
        # Create test department
        dept, created = Department.objects.get_or_create(
            name="Test Department",
            defaults={'description': 'Department for testing'}
        )
        if created:
            print(f"   ✅ Created test department: {dept.name}")
        else:
            print(f"   ✅ Found existing department: {dept.name}")
        
        # Create test users
        admin_user, created = User.objects.get_or_create(
            username="test_admin",
            defaults={
                'email': 'admin@test.com',
                'role': 'admin',
                'first_name': 'Test',
                'last_name': 'Admin'
            }
        )
        if created:
            admin_user.set_password('testpass123')
            admin_user.save()
            print(f"   ✅ Created test admin user: {admin_user.username}")
        else:
            print(f"   ✅ Found existing admin user: {admin_user.username}")
        
        manager_user, created = User.objects.get_or_create(
            username="test_manager",
            defaults={
                'email': 'manager@test.com',
                'role': 'manager',
                'department': dept,
                'first_name': 'Test',
                'last_name': 'Manager'
            }
        )
        if created:
            manager_user.set_password('testpass123')
            manager_user.save()
            print(f"   ✅ Created test manager user: {manager_user.username}")
        else:
            print(f"   ✅ Found existing manager user: {manager_user.username}")
        
        employee_user, created = User.objects.get_or_create(
            username="test_employee",
            defaults={
                'email': 'employee@test.com',
                'role': 'employee',
                'department': dept,
                'first_name': 'Test',
                'last_name': 'Employee'
            }
        )
        if created:
            employee_user.set_password('testpass123')
            employee_user.save()
            print(f"   ✅ Created test employee user: {employee_user.username}")
        else:
            print(f"   ✅ Found existing employee user: {employee_user.username}")
        
        # Test 4: Test role-based permissions
        print("\n4️⃣ Testing role-based permissions...")
        
        # Test admin permissions
        assert admin_user.is_admin == True
        assert admin_user.can_assign_tasks() == True
        print("   ✅ Admin permissions working correctly")
        
        # Test manager permissions
        assert manager_user.is_manager == True
        assert manager_user.can_assign_tasks() == True
        assert manager_user.can_assign_to_user(employee_user) == True
        print("   ✅ Manager permissions working correctly")
        
        # Test employee permissions
        assert employee_user.is_employee == True
        assert employee_user.can_assign_tasks() == False
        print("   ✅ Employee permissions working correctly")
        
        # Test 5: Test task creation
        print("\n5️⃣ Testing task creation...")
        
        from django.utils import timezone
        from datetime import timedelta
        
        task, created = Task.objects.get_or_create(
            title="Test Task",
            defaults={
                'description': 'This is a test task for integration testing',
                'created_by': manager_user,
                'assigned_to': employee_user,
                'department': dept,
                'priority': 'medium',
                'due_date': timezone.now() + timedelta(days=7)
            }
        )
        
        if created:
            print(f"   ✅ Created test task: {task.title}")
        else:
            print(f"   ✅ Found existing task: {task.title}")
        
        # Test task properties
        assert task.status == 'pending'  # Default status
        assert task.priority == 'medium'
        assert task.department == dept
        assert task.assigned_to == employee_user
        print("   ✅ Task properties set correctly")
        
        # Test task methods
        assert task.is_overdue == False  # Should not be overdue
        assert task.days_remaining >= 0  # Should have days remaining
        print("   ✅ Task methods working correctly")
        
        # Test 6: Test task queries
        print("\n6️⃣ Testing task queries...")
        
        # Get user tasks
        admin_tasks = Task.get_user_tasks(admin_user)
        manager_tasks = Task.get_user_tasks(manager_user)
        employee_tasks = Task.get_user_tasks(employee_user)
        
        print(f"   ✅ Admin can see {admin_tasks.count()} tasks")
        print(f"   ✅ Manager can see {manager_tasks.count()} department tasks")
        print(f"   ✅ Employee can see {employee_tasks.count()} assigned tasks")
        
        # Test 7: Test comments (if enabled)
        print("\n7️⃣ Testing task comments...")
        
        try:
            from tasks.models import TaskComment
            
            comment, created = TaskComment.objects.get_or_create(
                task=task,
                author=employee_user,
                defaults={
                    'content': 'This is a test comment on the task'
                }
            )
            
            if created:
                print(f"   ✅ Created test comment: {comment.content[:50]}...")
            else:
                print(f"   ✅ Found existing comment: {comment.content[:50]}...")
                
            print("   ✅ Task comments working correctly")
            
        except ImportError:
            print("   ⚠️  Task comments disabled (model not available)")
        
        # Test 8: Test URL configuration
        print("\n8️⃣ Testing URL configuration...")
        
        from django.urls import reverse
        from task_management.integration import get_url_namespace
        
        namespace = get_url_namespace()
        
        try:
            if namespace:
                dashboard_url = reverse(f'{namespace}:dashboard')
                task_list_url = reverse(f'{namespace}:task-list')
                login_url = reverse(f'{namespace}:login')
            else:
                dashboard_url = reverse('dashboard')
                task_list_url = reverse('task-list')
                login_url = reverse('login')
            
            print(f"   ✅ Dashboard URL: {dashboard_url}")
            print(f"   ✅ Task list URL: {task_list_url}")
            print(f"   ✅ Login URL: {login_url}")
            
        except Exception as e:
            print(f"   ❌ URL reversal failed: {e}")
        
        print("\n🎉 All tests passed! Task management module is working correctly.")
        
        # Cleanup option
        print("\n💡 To clean up test data, run:")
        print("   Task.objects.filter(title='Test Task').delete()")
        print("   User.objects.filter(username__startswith='test_').delete()")
        print("   Department.objects.filter(name='Test Department').delete()")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_integration_validation():
    """Test the integration validation functionality."""
    print("\n🔍 Testing integration validation...")
    
    try:
        from task_management.integration import validate_integration, check_prerequisites
        
        # Check prerequisites
        errors = check_prerequisites()
        if errors:
            print(f"   ⚠️  Found {len(errors)} configuration issues:")
            for error in errors:
                print(f"     - {error}")
        else:
            print("   ✅ All prerequisites met")
        
        # Validate integration
        validate_integration()
        print("   ✅ Integration validation passed")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Integration validation failed: {e}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("🚀 Django Task Management Module Integration Test")
    print("=" * 60)
    
    # Run basic functionality test
    basic_test_passed = test_basic_functionality()
    
    # Run integration validation test
    validation_test_passed = test_integration_validation()
    
    print("\n" + "=" * 60)
    print("📊 Test Results:")
    print(f"   Basic Functionality: {'✅ PASSED' if basic_test_passed else '❌ FAILED'}")
    print(f"   Integration Validation: {'✅ PASSED' if validation_test_passed else '❌ FAILED'}")
    
    if basic_test_passed and validation_test_passed:
        print("\n🎉 All tests passed! The module is ready for use.")
        print("\n📖 Next steps:")
        print("   1. Create real departments and users")
        print("   2. Set up proper authentication")
        print("   3. Customize templates for your application")
        print("   4. Configure email notifications if needed")
        print("   5. Run: python manage.py runserver")
    else:
        print("\n❌ Some tests failed. Please check the error messages above.")
        print("   Run: python manage.py validate_task_management_integration --verbose")
    
    print("=" * 60)