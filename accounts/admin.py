from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Department


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'user_count', 'created_at']
    search_fields = ['name', 'description']
    readonly_fields = ['created_at', 'updated_at']
    
    def user_count(self, obj):
        return obj.users.filter(is_active=True).count()
    user_count.short_description = 'Active Users'


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['username', 'get_full_name', 'role', 'department', 'employee_id', 'is_active', 'date_joined']
    list_filter = ['role', 'department', 'is_active', 'is_staff', 'date_joined']
    search_fields = ['username', 'first_name', 'last_name', 'email', 'employee_id', 'phone']
    readonly_fields = ['date_joined', 'last_login']
    
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Additional Information', {
            'fields': ('role', 'department', 'phone', 'employee_id')
        }),
    )
    
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Additional Information', {
            'fields': ('role', 'department', 'first_name', 'last_name', 'email')
        }),
    )
