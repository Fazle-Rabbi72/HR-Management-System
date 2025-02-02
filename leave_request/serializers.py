from rest_framework import serializers
from .models import Leave

class LeaveSerializer(serializers.ModelSerializer):
    total_days = serializers.ReadOnlyField()
    employee_name = serializers.CharField(source="employee.user.get_full_name", read_only=True)

    class Meta:
        model = Leave
        fields = ['id', 'employee','employee_name','start_date', 'end_date', 'reason', 'status', 'applied_on', 'total_days']
