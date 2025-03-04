from rest_framework import serializers
from .models import Leave

class LeaveSerializer(serializers.ModelSerializer):
    total_days = serializers.ReadOnlyField()
    employee_name = serializers.CharField(source="employee.user.get_full_name", read_only=True)
    designation=serializers.CharField(source="employee.designation", read_only=True)
    department=serializers.CharField(source="employee.department", read_only=True)
    status = serializers.CharField(read_only=True)

    class Meta:
        model = Leave
        fields = ['id', 'employee','employee_name','designation','department','start_date', 'end_date', 'reason', 'status', 'applied_on', 'total_days']
