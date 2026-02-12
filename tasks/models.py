from django.db import models
from django.urls import reverse
from django.core.exceptions import ValidationError
from django.utils import timezone
from .settings import STATUS_CHOICES, PRIORITY_CHOICES, DEFAULT_STATUS, DEFAULT_PRIORITY, ALLOW_COMMENTS, AUTO_COMPLETE_ON_STATUS_CHANGE


class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    created_by = models.ForeignKey(
        'accounts.User',
        on_delete=models.CASCADE,
        related_name='created_tasks'
    )
    assigned_to = models.ForeignKey(
        'accounts.User',
        on_delete=models.CASCADE,
        related_name='assigned_tasks',
        null=True,
        blank=True
    )
    department = models.ForeignKey(
        'accounts.Department',
        on_delete=models.CASCADE,
        related_name='tasks'
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=DEFAULT_STATUS
    )
    priority = models.CharField(
        max_length=20,
        choices=PRIORITY_CHOICES,
        default=DEFAULT_PRIORITY
    )
    due_date = models.DateTimeField()
    completed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} - {self.get_status_display()}"

    def get_absolute_url(self):
        return reverse('task-detail', kwargs={'pk': self.pk})

    def clean(self):
        # Validate that due_date is in the future
        if self.due_date and self.due_date < timezone.now():
            if not self.pk:  # Only validate for new tasks
                raise ValidationError({'due_date': 'Due date must be in the future.'})
        
        # Validate that the assigned user is in the same department
        if self.assigned_to and self.assigned_to.department != self.department:
            raise ValidationError({
                'assigned_to': 'Assigned user must be in the same department as the task.'
            })
        
        # Validate that the creator can assign to this user
        if self.assigned_to and hasattr(self, 'created_by'):
            if not self.created_by.can_assign_to_user(self.assigned_to):
                raise ValidationError({
                    'assigned_to': 'You do not have permission to assign tasks to this user.'
                })

    def save(self, *args, **kwargs):
        # Update completed_at when status changes to completed
        if AUTO_COMPLETE_ON_STATUS_CHANGE:
            if self.status == 'completed' and not self.completed_at:
                self.completed_at = timezone.now()
            elif self.status != 'completed':
                self.completed_at = None
        
        self.full_clean()
        super().save(*args, **kwargs)

    @property
    def is_overdue(self):
        if self.status == 'completed':
            return False
        return timezone.now() > self.due_date

    @property
    def days_remaining(self):
        if self.status == 'completed':
            return 0
        delta = self.due_date - timezone.now()
        return max(0, delta.days)

    @classmethod
    def get_department_tasks(cls, department):
        """Get all tasks for a specific department"""
        return cls.objects.filter(department=department)

    @classmethod
    def get_user_tasks(cls, user):
        """Get tasks visible to a user based on their role"""
        if user.is_admin:
            return cls.objects.all()
        elif user.is_manager:
            return cls.objects.filter(department=user.department)
        else:
            return cls.objects.filter(assigned_to=user)


# Only create TaskComment model if comments are enabled
if ALLOW_COMMENTS:
    class TaskComment(models.Model):
        task = models.ForeignKey(
            Task,
            on_delete=models.CASCADE,
            related_name='comments'
        )
        author = models.ForeignKey(
            'accounts.User',
            on_delete=models.CASCADE,
            related_name='task_comments'
        )
        content = models.TextField()
        created_at = models.DateTimeField(auto_now_add=True)
        updated_at = models.DateTimeField(auto_now=True)

        class Meta:
            ordering = ['-created_at']

        def __str__(self):
            return f"Comment by {self.author} on {self.task.title}"