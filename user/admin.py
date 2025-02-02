from django.contrib import admin
from .models import User, Employee

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'role', 'is_staff', 'is_active')
    search_fields = ('username', 'email')  
    ordering = ('id',)
    
    # Use autocomplete to improve performance
    autocomplete_fields = ['role']

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'department', 'designation', 'date_of_joining', 'phone')
    list_filter = ('department', 'designation')
    search_fields = ('user__username', 'user__email')
    ordering = ('id',)

    # Optimize ForeignKey selection
    autocomplete_fields = ['user']
