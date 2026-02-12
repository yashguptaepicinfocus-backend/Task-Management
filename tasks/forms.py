from django import forms
from django.utils import timezone
from .models import Task, TaskComment
from accounts.models import User, Department


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'department', 'assigned_to', 'priority', 'due_date']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'department': forms.Select(attrs={'class': 'form-control'}),
            'assigned_to': forms.Select(attrs={'class': 'form-control'}),
            'priority': forms.Select(attrs={'class': 'form-control'}),
            'due_date': forms.DateTimeInput(
                attrs={'class': 'form-control', 'type': 'datetime-local'},
                format='%Y-%m-%dT%H:%M'
            ),
        }

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        
        if user:
            # Filter departments based on user role
            if user.is_manager:
                self.fields['department'].queryset = Department.objects.filter(id=user.department_id)
                self.fields['department'].initial = user.department
            elif user.is_admin:
                self.fields['department'].queryset = Department.objects.all()
            
            # Filter assignable users based on department
            if user.is_manager and user.department:
                self.fields['assigned_to'].queryset = User.objects.filter(
                    department=user.department,
                    role='employee',
                    is_active=True
                )
            elif user.is_admin:
                self.fields['assigned_to'].queryset = User.objects.filter(
                    role='employee',
                    is_active=True
                )

    def clean_due_date(self):
        due_date = self.cleaned_data.get('due_date')
        if due_date and due_date < timezone.now():
            raise forms.ValidationError('Due date must be in the future.')
        return due_date

    def clean(self):
        cleaned_data = super().clean()
        department = cleaned_data.get('department')
        assigned_to = cleaned_data.get('assigned_to')
        
        # Validate that assigned user is in the selected department
        if assigned_to and department:
            if assigned_to.department != department:
                raise forms.ValidationError(
                    'The assigned user must belong to the selected department.'
                )
        
        # Validate user permissions
        if self.user and not self.user.is_admin:
            if department and self.user.department != department:
                raise forms.ValidationError(
                    'You can only create tasks in your own department.'
                )
        
        return cleaned_data


class TaskStatusForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['status']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-control'}),
        }


class TaskCommentForm(forms.ModelForm):
    class Meta:
        model = TaskComment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Add a comment...'
            }),
        }
