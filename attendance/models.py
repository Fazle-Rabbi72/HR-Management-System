from django.db import models
from django.contrib.auth import get_user_model
from datetime import timedelta
from user.models import User

# Attendance Model
class Attendance(models.Model):
    STATUS_CHOICES = (
        ('Present', 'Present'),
        ('Absent', 'Absent'),
    )
    employee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='attendances')
    date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    punch_in = models.DateTimeField(null=True, blank=True)  # Punch-in time
    punch_out = models.DateTimeField(null=True, blank=True)  # Punch-out time

    def total_working_hours(self):
        """Calculate total working hours between punch-in and punch-out."""
        if self.punch_in and self.punch_out:
            duration = self.punch_out - self.punch_in
            # Convert to hours and minutes
            total_seconds = duration.total_seconds()
            hours = total_seconds // 3600
            minutes = (total_seconds % 3600) // 60
            return f"{int(hours)} hours, {int(minutes)} minutes"
        return "Not available"

    def __str__(self):
        return f"{self.employee.username} - {self.date} - {self.status}"
