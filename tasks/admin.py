from django.contrib import admin
from .models import Task, TaskComment


class TaskCommentInline(admin.TabularInline):
    model = TaskComment
    extra = 0
    readonly_fields = ['author', 'created_at']
    fields = ['author', 'content', 'created_at']


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['title', 'department', 'assigned_to', 'status', 'priority', 'due_date', 'is_overdue', 'created_by']
    list_filter = ['status', 'priority', 'department', 'created_at', 'due_date']
    search_fields = ['title', 'description', 'assigned_to__username', 'assigned_to__first_name', 'assigned_to__last_name']
    readonly_fields = ['created_at', 'updated_at', 'completed_at', 'is_overdue', 'days_remaining']
    date_hierarchy = 'due_date'
    inlines = [TaskCommentInline]
    
    fieldsets = (
        ('Task Information', {
            'fields': ('title', 'description', 'department')
        }),
        ('Assignment', {
            'fields': ('created_by', 'assigned_to')
        }),
        ('Status & Priority', {
            'fields': ('status', 'priority', 'due_date', 'completed_at')
        }),
        ('Statistics', {
            'fields': ('is_overdue', 'days_remaining'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_admin:
            return qs
        elif request.user.is_manager:
            return qs.filter(department=request.user.department)
        return qs.filter(assigned_to=request.user)


@admin.register(TaskComment)
class TaskCommentAdmin(admin.ModelAdmin):
    list_display = ['task', 'author', 'short_content', 'created_at']
    list_filter = ['created_at', 'task__department']
    search_fields = ['content', 'task__title', 'author__username']
    readonly_fields = ['created_at', 'updated_at']
    
    def short_content(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    short_content.short_description = 'Content'
