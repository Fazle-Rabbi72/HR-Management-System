from django.db import models
from user.models import Employee  # Assuming Employee model exists
from datetime import date

class Payroll(models.Model):
    employee = models.OneToOneField(Employee, on_delete=models.CASCADE, related_name="payroll")
    basic_salary = models.DecimalField(max_digits=10, decimal_places=2)
    bonus = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    deductions = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    tax = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def calculate_net_salary(self):
        return self.basic_salary + self.bonus - self.deductions - self.tax

    def __str__(self):
        return f"{self.employee.user.first_name} {self.employee.user.last_name} - Payroll"

class Payslip(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="payslips")
    month = models.CharField(max_length=20, choices=[
        ("January", "January"), ("February", "February"), ("March", "March"), 
        ("April", "April"), ("May", "May"), ("June", "June"), ("July", "July"), 
        ("August", "August"), ("September", "September"), ("October", "October"),
        ("November", "November"), ("December", "December")
    ])
    year = models.IntegerField(default=date.today().year)
    basic_salary = models.DecimalField(max_digits=10, decimal_places=2)
    bonus = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    deductions = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    tax = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    net_salary = models.DecimalField(max_digits=10, decimal_places=2)
    paid = models.BooleanField(default=False)  # ✅ Payment status track

    def __str__(self):
        return f"{self.employee.user.first_name} {self.employee.user.last_name} - Payslip ({self.month} {self.year})"
