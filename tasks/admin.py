from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Organization, Team, Task, CustomUser

class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'phone_number', 'role', 'is_staff', 'is_active')
    search_fields = ('email', 'first_name', 'last_name')
    list_filter = ('is_staff', 'is_active', 'role')
    ordering = ('email',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'phone_number', 'address')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'role', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'phone_number', 'role', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'organization', 'created_at')
    search_fields = ('name', 'organization__name')

class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'assigned_to','assigned_by','team','status','completed')
    search_fields = ('title', 'assigned_to__first_name')
    list_filter = ('status',)
    
    def save_model(self, request, obj, form, change):
        if request.user.role != 'team_lead':
            raise PermissionError("Only Team Leads can assign tasks.")
        super().save_model(request, obj, form, change)

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Organization)
admin.site.register(Team, TeamAdmin)
admin.site.register(Task, TaskAdmin)