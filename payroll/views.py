from django.core.mail import send_mail
from django.conf import settings
from rest_framework import viewsets
from rest_framework.response import Response
from datetime import date
from .models import Payroll, Payslip
from .serializers import PayrollSerializer, PayslipSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

class PayrollViewSet(viewsets.ModelViewSet):
    queryset = Payroll.objects.all()
    serializer_class = PayrollSerializer

def send_payslip_email(payslip, paid=False):
    """Payslip Generate বা Paid হলে Employee-কে Email পাঠানোর ফাংশন"""
    subject = f"Payslip for {payslip.month} {payslip.year} - {'Paid' if paid else 'Generated'}"
    
    message = f"""
    Dear {payslip.employee.user.first_name},

    Your payslip for {payslip.month} {payslip.year} has been {'approved and paid' if paid else 'generated'}.

    Salary Details:
    - Basic Salary: {payslip.basic_salary}
    - Bonus: {payslip.bonus}
    - Deductions: {payslip.deductions}
    - Tax: {payslip.tax}
    - Net Salary: {payslip.net_salary}
    - Paid Status: {"Paid" if payslip.paid else "Unpaid"}

    Best regards,
    HR Department
    """

    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [payslip.employee.user.email],
        fail_silently=False,
    )

class PayslipViewSet(viewsets.ModelViewSet):
    queryset = Payslip.objects.all()
    serializer_class = PayslipSerializer
    filter_backends = [DjangoFilterBackend ,filters.SearchFilter]  
    filterset_fields = ["employee", "year"]  

    def create(self, request, *args, **kwargs):
        employee_id = request.data.get('employee')
        month = request.data.get('month')
        year = request.data.get('year', date.today().year)

        try:
            payroll = Payroll.objects.get(employee_id=employee_id)
        except Payroll.DoesNotExist:
            return Response({"error": "Payroll record not found for this employee."}, status=400)

        net_salary = payroll.calculate_net_salary()

        payslip = Payslip.objects.create(
            employee_id=employee_id,
            month=month,
            year=year,
            basic_salary=payroll.basic_salary,
            bonus=payroll.bonus,
            deductions=payroll.deductions,
            tax=payroll.tax,
            net_salary=net_salary
        )

        send_payslip_email(payslip)

        serializer = PayslipSerializer(payslip)
        return Response(serializer.data)
