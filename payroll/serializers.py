from rest_framework import serializers
from .models import Payroll, Payslip

class PayrollSerializer(serializers.ModelSerializer):
    employee_username = serializers.CharField(source="employee.user.username", read_only=True)
    employee_name=serializers.CharField(source="employee.user.get_full_name", read_only=True)
    class Meta:
        model = Payroll
        fields = "__all__"

class PayslipSerializer(serializers.ModelSerializer):
    employee_name = serializers.CharField(source="employee.user.get_full_name", read_only=True)

    class Meta:
        model = Payslip
        fields = "__all__"
        read_only_fields = ["net_salary"]
