from django.contrib import admin
from .models import Leave

@admin.register(Leave)
class LeaveAdmin(admin.ModelAdmin):
    list_display = ('employee', 'start_date', 'end_date', 'status', 'total_days', 'applied_on')
    list_filter = ('status', 'start_date', 'end_date', 'applied_on')
    search_fields = ('employee__username', 'reason')
    ordering = ('-applied_on',)
    readonly_fields = ('total_days', 'applied_on')

    def total_days(self, obj):
        return obj.total_days()
    total_days.short_description = 'Total Days'
