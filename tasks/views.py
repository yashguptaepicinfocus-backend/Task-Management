from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.utils import timezone
from .models import Task, TaskComment
from .forms import TaskForm, TaskStatusForm, TaskCommentForm
from accounts.models import User


@login_required
def task_list(request):
    """List tasks based on user role"""
    user = request.user
    
    if user.is_admin:
        tasks = Task.objects.select_related('assigned_to', 'department', 'created_by').all()
    elif user.is_manager:
        tasks = Task.objects.filter(department=user.department).select_related('assigned_to', 'created_by')
    else:
        tasks = Task.objects.filter(assigned_to=user).select_related('department', 'created_by')
    
    # Filter by status
    status = request.GET.get('status')
    if status:
        tasks = tasks.filter(status=status)
    
    # Filter by priority
    priority = request.GET.get('priority')
    if priority:
        tasks = tasks.filter(priority=priority)
    
    # Filter by assigned user (for managers and admins)
    assigned_to = request.GET.get('assigned_to')
    if assigned_to and (user.is_admin or user.is_manager):
        tasks = tasks.filter(assigned_to_id=assigned_to)
    
    # Search
    search = request.GET.get('search')
    if search:
        tasks = tasks.filter(
            Q(title__icontains=search) | Q(description__icontains=search)
        )
    
    context = {
        'tasks': tasks,
        'status_choices': Task.STATUS_CHOICES,
        'priority_choices': Task.PRIORITY_CHOICES,
    }
    
    if user.can_assign_tasks():
        context['assignable_users'] = user.get_managed_users()
    
    return render(request, 'tasks/task_list.html', context)


@login_required
def task_detail(request, pk):
    """View task details"""
    task = get_object_or_404(Task, pk=pk)
    user = request.user
    
    # Check permissions
    if not user.is_admin:
        if user.is_manager and task.department != user.department:
            raise PermissionDenied
        elif user.is_employee and task.assigned_to != user:
            raise PermissionDenied
    
    comments = task.comments.select_related('author').all()
    
    if request.method == 'POST':
        comment_form = TaskCommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.task = task
            comment.author = user
            comment.save()
            messages.success(request, 'Comment added successfully.')
            return redirect('task-detail', pk=pk)
    else:
        comment_form = TaskCommentForm()
    
    context = {
        'task': task,
        'comments': comments,
        'comment_form': comment_form,
        'can_edit': user.can_assign_tasks() and (user.is_admin or task.created_by == user),
        'can_update_status': task.assigned_to == user or user.can_assign_tasks(),
    }
    
    return render(request, 'tasks/task_detail.html', context)


@login_required
def task_create(request):
    """Create a new task"""
    user = request.user
    
    if not user.can_assign_tasks():
        raise PermissionDenied
    
    if request.method == 'POST':
        form = TaskForm(request.POST, user=user)
        if form.is_valid():
            task = form.save(commit=False)
            task.created_by = user
            
            # Validate department permission
            if user.is_manager and task.department != user.department:
                messages.error(request, 'You can only create tasks in your own department.')
                return render(request, 'tasks/task_form.html', {'form': form})
            
            # Validate assignment permission
            if task.assigned_to and not user.can_assign_to_user(task.assigned_to):
                messages.error(request, 'You cannot assign tasks to this user.')
                return render(request, 'tasks/task_form.html', {'form': form})
            
            task.save()
            messages.success(request, f'Task "{task.title}" created successfully.')
            return redirect('task-detail', pk=task.pk)
    else:
        form = TaskForm(user=user)
    
    return render(request, 'tasks/task_form.html', {'form': form, 'action': 'Create'})


@login_required
def task_update(request, pk):
    """Update an existing task"""
    task = get_object_or_404(Task, pk=pk)
    user = request.user
    
    # Check permissions
    if not user.can_assign_tasks():
        raise PermissionDenied
    
    if user.is_manager:
        if task.department != user.department:
            raise PermissionDenied
        if task.created_by != user and not user.is_admin:
            raise PermissionDenied
    
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task, user=user)
        if form.is_valid():
            updated_task = form.save(commit=False)
            
            # Validate assignment permission
            if updated_task.assigned_to and not user.can_assign_to_user(updated_task.assigned_to):
                messages.error(request, 'You cannot assign tasks to this user.')
                return render(request, 'tasks/task_form.html', {'form': form, 'action': 'Update'})
            
            updated_task.save()
            messages.success(request, f'Task "{updated_task.title}" updated successfully.')
            return redirect('task-detail', pk=task.pk)
    else:
        form = TaskForm(instance=task, user=user)
    
    return render(request, 'tasks/task_form.html', {'form': form, 'action': 'Update', 'task': task})


@login_required
def task_delete(request, pk):
    """Delete a task"""
    task = get_object_or_404(Task, pk=pk)
    user = request.user
    
    # Check permissions
    if not user.can_assign_tasks():
        raise PermissionDenied
    
    if user.is_manager:
        if task.department != user.department:
            raise PermissionDenied
        if task.created_by != user:
            raise PermissionDenied
    
    if request.method == 'POST':
        task_title = task.title
        task.delete()
        messages.success(request, f'Task "{task_title}" deleted successfully.')
        return redirect('task-list')
    
    return render(request, 'tasks/task_confirm_delete.html', {'task': task})


@login_required
def task_update_status(request, pk):
    """Update task status (for assigned employees or managers)"""
    task = get_object_or_404(Task, pk=pk)
    user = request.user
    
    # Check permissions
    if not (user.is_admin or task.assigned_to == user or 
            (user.is_manager and task.department == user.department)):
        raise PermissionDenied
    
    if request.method == 'POST':
        form = TaskStatusForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, f'Task status updated to {task.get_status_display()}.')
            return redirect('task-detail', pk=pk)
    else:
        form = TaskStatusForm(instance=task)
    
    return render(request, 'tasks/task_status_form.html', {'form': form, 'task': task})


@login_required
def my_tasks(request):
    """View tasks assigned to current user"""
    tasks = Task.objects.filter(assigned_to=request.user).select_related('department', 'created_by')
    
    context = {
        'tasks': tasks,
        'status_choices': Task.STATUS_CHOICES,
        'page_title': 'My Tasks'
    }
    
    return render(request, 'tasks/task_list.html', context)
