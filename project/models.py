from django.db import models
from user.models import Employee , Department

# Create your models here.

class Client(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    address = models.TextField()

    def __str__(self):
        return self.name


class Project(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    status = models.CharField(
        max_length=20,
        choices=[("Ongoing", "Ongoing"), ("Completed", "Completed"), ("Cancelled", "Cancelled")],
        default="Ongoing"
    )
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="projects")

    def __str__(self):
        return self.name

class Team(models.Model):
    project = models.OneToOneField(Project, on_delete=models.CASCADE, related_name="team")
    leader = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, related_name="leading_teams")
    members = models.ManyToManyField(Employee, related_name="teams")

    def __str__(self):
        return f"Team for {self.project.name}"
