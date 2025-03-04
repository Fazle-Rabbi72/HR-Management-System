from rest_framework import serializers
from .models import Attendance

class AttendanceSerializer(serializers.ModelSerializer):
    total_working_hours = serializers.SerializerMethodField()
    employee_name = serializers.CharField(source="employee.user.get_full_name", read_only=True)

    class Meta:
        model = Attendance
        fields = ['id', 'employee','employee_name', 'date', 'status', 'punch_in', 'punch_out', 'total_working_hours']

    def get_total_working_hours(self, obj):
        return obj.total_working_hours()
