from rest_framework import serializers
from .models import Leave

class LeaveSerializer(serializers.ModelSerializer):
    total_days = serializers.IntegerField(read_only=True)  # Remove source
    employee_name=serializers.ReadOnlyField(source='employee.username')

    class Meta:
        model = Leave
        fields = ['id', 'employee','employee_name', 'start_date', 'end_date', 'reason', 'status', 'total_days']
        read_only_fields = ['employee', 'status', 'total_days']
