from rest_framework import serializers
from .models import Leave

class LeaveSerializer(serializers.ModelSerializer):
    total_days = serializers.ReadOnlyField()

    class Meta:
        model = Leave
        fields = ['id', 'employee', 'start_date', 'end_date', 'reason', 'status', 'applied_on', 'total_days']
