from django.contrib import admin
from .models import User, Employee

# Customizing the User model admin panel
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'role', 'is_staff', 'is_active')
    list_filter = ('role', 'is_staff', 'is_active')
    search_fields = ('username', 'email', 'role')
    ordering = ('id',)

# Customizing the Employee model admin panel
@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'department', 'designation', 'date_of_joining', 'phone')
    list_filter = ('department', 'designation')
    search_fields = ('user__username', 'user__email', 'department', 'designation')
    ordering = ('id',)
    autocomplete_fields = ['user']  # Enable autocomplete for User field
