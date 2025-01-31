from django.contrib import admin
from .models import Payroll, Payslip

@admin.register(Payroll)
class PayrollAdmin(admin.ModelAdmin):
    list_display = ("employee", "basic_salary", "bonus", "deductions", "tax")
    search_fields = ("employee__user__first_name", "employee__user__last_name")
    list_filter = ("employee",)

@admin.register(Payslip)
class PayslipAdmin(admin.ModelAdmin):
    list_display = ("employee", "month", "year", "net_salary", "paid")
    search_fields = ("employee__user__first_name", "employee__user__last_name", "month", "year")
    list_filter = ("month", "year", "paid")
    actions = ["mark_as_paid"]

    