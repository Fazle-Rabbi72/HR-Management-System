from rest_framework import serializers
from .models import Attendance

class AttendanceSerializer(serializers.ModelSerializer):
    total_working_hours = serializers.SerializerMethodField()

    class Meta:
        model = Attendance
        fields = ['id', 'employee', 'date', 'status', 'punch_in', 'punch_out', 'total_working_hours']

    def get_total_working_hours(self, obj):
        return obj.total_working_hours()
