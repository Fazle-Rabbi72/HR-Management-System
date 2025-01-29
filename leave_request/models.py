from django.db import models
from user.models import User

class Leave(models.Model):
    employee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='leaves')
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    reason = models.TextField()
    status = models.CharField(
        max_length=10,
        choices=(
            ('Pending', 'Pending'),
            ('Approved', 'Approved'),
            ('Rejected', 'Rejected'),
        ),
        default='Pending',
    )
    applied_on = models.DateTimeField(auto_now_add=True)

    def total_days(self):
        if self.start_date and self.end_date:
            return (self.end_date - self.start_date).days + 1
        return 0

    def __str__(self):
        return f"{self.employee.username} - {self.start_date} to {self.end_date} ({self.status})"
