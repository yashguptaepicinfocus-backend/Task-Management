from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta
from accounts.models import Department, User
from tasks.models import Task, TaskComment


User = get_user_model()


class DepartmentModelTest(TestCase):
    def setUp(self):
        self.department = Department.objects.create(
            name='IT Department',
            description='Information Technology'
        )

    def test_department_creation(self):
        self.assertEqual(self.department.name, 'IT Department')
        self.assertEqual(str(self.department), 'IT Department')

    def test_department_ordering(self):
        dept2 = Department.objects.create(name='HR Department')
        departments = list(Department.objects.all())
        self.assertEqual(departments[0].name, 'HR Department')
        self.assertEqual(departments[1].name, 'IT Department')


class UserModelTest(TestCase):
    def setUp(self):
        self.department = Department.objects.create(name='IT')
        self.admin = User.objects.create_user(
            username='admin',
            password='testpass123',
            role='admin'
        )
        self.manager = User.objects.create_user(
            username='manager',
            password='testpass123',
            role='manager',
            department=self.department
        )
        self.employee = User.objects.create_user(
            username='employee',
            password='testpass123',
            role='employee',
            department=self.department
        )

    def test_user_role_properties(self):
        self.assertTrue(self.admin.is_admin)
        self.assertFalse(self.admin.is_manager)
        self.assertFalse(self.admin.is_employee)
        
        self.assertTrue(self.manager.is_manager)
        self.assertFalse(self.manager.is_admin)
        
        self.assertTrue(self.employee.is_employee)
        self.assertFalse(self.employee.is_manager)

    def test_can_assign_tasks(self):
        self.assertTrue(self.admin.can_assign_tasks())
        self.assertTrue(self.manager.can_assign_tasks())
        self.assertFalse(self.employee.can_assign_tasks())

    def test_can_assign_to_user(self):
        # Admin can assign to anyone
        self.assertTrue(self.admin.can_assign_to_user(self.employee))
        
        # Manager can only assign within department
        self.assertTrue(self.manager.can_assign_to_user(self.employee))
        
        # Create employee in different department
        other_dept = Department.objects.create(name='HR')
        other_employee = User.objects.create_user(
            username='other_employee',
            password='testpass123',
            role='employee',
            department=other_dept
        )
        self.assertFalse(self.manager.can_assign_to_user(other_employee))

    def test_get_managed_users(self):
        # Admin sees all users
        admin_managed = self.admin.get_managed_users()
        self.assertIn(self.employee, admin_managed)
        self.assertIn(self.manager, admin_managed)
        
        # Manager sees only department users
        manager_managed = self.manager.get_managed_users()
        self.assertIn(self.employee, manager_managed)
        self.assertNotIn(self.admin, manager_managed)


class TaskModelTest(TestCase):
    def setUp(self):
        self.department = Department.objects.create(name='IT')
        self.manager = User.objects.create_user(
            username='manager',
            password='testpass123',
            role='manager',
            department=self.department
        )
        self.employee = User.objects.create_user(
            username='employee',
            password='testpass123',
            role='employee',
            department=self.department
        )
        self.task = Task.objects.create(
            title='Test Task',
            description='Test Description',
            created_by=self.manager,
            assigned_to=self.employee,
            department=self.department,
            priority='high',
            due_date=timezone.now() + timedelta(days=7)
        )

    def test_task_creation(self):
        self.assertEqual(self.task.title, 'Test Task')
        self.assertEqual(self.task.status, 'pending')
        self.assertEqual(str(self.task), 'Test Task - Pending')

    def test_task_status_transitions(self):
        # Test completing task sets completed_at
        self.task.status = 'completed'
        self.task.save()
        self.assertIsNotNone(self.task.completed_at)
        
        # Test reopening task clears completed_at
        self.task.status = 'in_progress'
        self.task.save()
        self.assertIsNone(self.task.completed_at)

    def test_is_overdue(self):
        # Future task not overdue
        self.assertFalse(self.task.is_overdue)
        
        # Past task is overdue
        self.task.due_date = timezone.now() - timedelta(days=1)
        self.task.save()
        self.assertTrue(self.task.is_overdue)
        
        # Completed task is never overdue
        self.task.status = 'completed'
        self.task.save()
        self.assertFalse(self.task.is_overdue)

    def test_cross_department_assignment_validation(self):
        other_dept = Department.objects.create(name='HR')
        other_employee = User.objects.create_user(
            username='other_employee',
            password='testpass123',
            role='employee',
            department=other_dept
        )
        
        with self.assertRaises(Exception):
            Task.objects.create(
                title='Invalid Task',
                description='Description',
                created_by=self.manager,
                assigned_to=other_employee,
                department=self.department,
                due_date=timezone.now() + timedelta(days=7)
            )


class TaskCommentModelTest(TestCase):
    def setUp(self):
        self.department = Department.objects.create(name='IT')
        self.manager = User.objects.create_user(
            username='manager',
            password='testpass123',
            role='manager',
            department=self.department
        )
        self.employee = User.objects.create_user(
            username='employee',
            password='testpass123',
            role='employee',
            department=self.department
        )
        self.task = Task.objects.create(
            title='Test Task',
            description='Description',
            created_by=self.manager,
            assigned_to=self.employee,
            department=self.department,
            due_date=timezone.now() + timedelta(days=7)
        )
        self.comment = TaskComment.objects.create(
            task=self.task,
            author=self.employee,
            content='Test comment'
        )

    def test_comment_creation(self):
        self.assertEqual(self.comment.content, 'Test comment')
        self.assertEqual(self.comment.author, self.employee)
        self.assertEqual(self.comment.task, self.task)


class ViewAccessControlTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.department = Department.objects.create(name='IT')
        self.admin = User.objects.create_user(
            username='admin',
            password='testpass123',
            role='admin'
        )
        self.manager = User.objects.create_user(
            username='manager',
            password='testpass123',
            role='manager',
            department=self.department
        )
        self.employee = User.objects.create_user(
            username='employee',
            password='testpass123',
            role='employee',
            department=self.department
        )
        self.task = Task.objects.create(
            title='Test Task',
            description='Description',
            created_by=self.manager,
            assigned_to=self.employee,
            department=self.department,
            due_date=timezone.now() + timedelta(days=7)
        )

    def test_employee_cannot_create_task(self):
        self.client.login(username='employee', password='testpass123')
        response = self.client.get('/tasks/create/')
        self.assertEqual(response.status_code, 403)

    def test_employee_can_view_assigned_task(self):
        self.client.login(username='employee', password='testpass123')
        response = self.client.get(f'/tasks/{self.task.pk}/')
        self.assertEqual(response.status_code, 200)

    def test_manager_can_create_task(self):
        self.client.login(username='manager', password='testpass123')
        response = self.client.get('/tasks/create/')
        self.assertEqual(response.status_code, 200)

    def test_cross_department_access_denied(self):
        # Create task in different department
        other_dept = Department.objects.create(name='HR')
        other_manager = User.objects.create_user(
            username='other_manager',
            password='testpass123',
            role='manager',
            department=other_dept
        )
        other_task = Task.objects.create(
            title='Other Task',
            description='Description',
            created_by=other_manager,
            department=other_dept,
            due_date=timezone.now() + timedelta(days=7)
        )
        
        # Manager cannot access task from other department
        self.client.login(username='manager', password='testpass123')
        response = self.client.get(f'/tasks/{other_task.pk}/')
        self.assertEqual(response.status_code, 403)

    def test_admin_can_access_all_tasks(self):
        self.client.login(username='admin', password='testpass123')
        response = self.client.get(f'/tasks/{self.task.pk}/')
        self.assertEqual(response.status_code, 200)

    def test_login_required(self):
        # Test that login is required for protected views
        response = self.client.get('/')
        self.assertEqual(response.status_code, 302)  # Redirect to login
        
        response = self.client.get('/tasks/')
        self.assertEqual(response.status_code, 302)  # Redirect to login
