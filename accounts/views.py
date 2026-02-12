from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count, Q
from django.utils import timezone
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from tasks.models import Task


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Welcome back, {user.get_full_name() or user.username}!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = CustomAuthenticationForm()
    
    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('login')


@login_required
def dashboard(request):
    user = request.user
    context = {}
    
    if user.is_admin:
        # Admin sees all statistics
        context['total_tasks'] = Task.objects.count()
        context['completed_tasks'] = Task.objects.filter(status='completed').count()
        context['pending_tasks'] = Task.objects.filter(status='pending').count()
        context['in_progress_tasks'] = Task.objects.filter(status='in_progress').count()
        context['overdue_tasks'] = Task.objects.filter(
            due_date__lt=timezone.now()
        ).exclude(status='completed').count()
        context['recent_tasks'] = Task.objects.select_related('assigned_to', 'department').all()[:10]
        
    elif user.is_manager:
        # Manager sees department statistics
        dept_tasks = Task.objects.filter(department=user.department)
        context['total_tasks'] = dept_tasks.count()
        context['completed_tasks'] = dept_tasks.filter(status='completed').count()
        context['pending_tasks'] = dept_tasks.filter(status='pending').count()
        context['in_progress_tasks'] = dept_tasks.filter(status='in_progress').count()
        context['overdue_tasks'] = dept_tasks.filter(
            due_date__lt=timezone.now()
        ).exclude(status='completed').count()
        context['department_users'] = user.get_managed_users()
        context['recent_tasks'] = dept_tasks.select_related('assigned_to')[:10]
        
    else:
        # Employee sees their assigned tasks
        assigned_tasks = Task.objects.filter(assigned_to=user)
        context['total_tasks'] = assigned_tasks.count()
        context['completed_tasks'] = assigned_tasks.filter(status='completed').count()
        context['pending_tasks'] = assigned_tasks.filter(status='pending').count()
        context['in_progress_tasks'] = assigned_tasks.filter(status='in_progress').count()
        context['overdue_tasks'] = assigned_tasks.filter(
            due_date__lt=timezone.now()
        ).exclude(status='completed').count()
        context['assigned_tasks'] = assigned_tasks.select_related('department')[:10]
    
    return render(request, 'accounts/dashboard.html', context)


@login_required
def profile_view(request):
    return render(request, 'accounts/profile.html', {'user': request.user})
