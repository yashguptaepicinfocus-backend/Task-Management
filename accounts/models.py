from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.conf import settings as django_settings
from .settings import ROLE_CHOICES, DEFAULT_ROLE


class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('department-detail', kwargs={'pk': self.pk})


class User(AbstractUser):
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=DEFAULT_ROLE)
    department = models.ForeignKey(
        Department,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='users'
    )
    phone = models.CharField(max_length=20, blank=True)
    employee_id = models.CharField(max_length=50, unique=True, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['first_name', 'last_name']

    def __str__(self):
        return f"{self.get_full_name()} ({self.username})"

    def get_absolute_url(self):
        return reverse('user-detail', kwargs={'pk': self.pk})

    @property
    def is_admin(self):
        return self.role == 'admin' or self.is_superuser

    @property
    def is_manager(self):
        return self.role == 'manager'

    @property
    def is_employee(self):
        return self.role == 'employee'

    def can_assign_tasks(self):
        return self.is_admin or self.is_manager

    def can_assign_to_user(self, user):
        """Check if this user can assign tasks to the given user"""
        if self.is_admin:
            return True
        if self.is_manager and user.department == self.department:
            return True
        return False

    def get_managed_users(self):
        """Get users that this user can assign tasks to"""
        if self.is_admin:
            return User.objects.filter(is_active=True)
        if self.is_manager and self.department:
            return User.objects.filter(department=self.department, is_active=True)
        return User.objects.none()