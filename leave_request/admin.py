from django.contrib import admin
from .models import Leave

@admin.register(Leave)
class LeaveAdmin(admin.ModelAdmin):
    list_display = ('employee', 'start_date', 'end_date', 'status', 'applied_on')
    list_filter = ('status', 'start_date', 'end_date')
    search_fields = ('employee__username', 'status')

