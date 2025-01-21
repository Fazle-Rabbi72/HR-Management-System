from django.contrib import admin
from .models import Attendance

class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('employee', 'date', 'status', 'punch_in', 'punch_out', 'get_total_working_hours')

    def get_total_working_hours(self, obj):
        return obj.total_working_hours()

    get_total_working_hours.short_description = "Total Working Hours"

admin.site.register(Attendance, AttendanceAdmin)
