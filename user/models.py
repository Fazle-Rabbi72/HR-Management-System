from django.db import models
from django.contrib.auth.models import AbstractUser
from cloudinary.models import CloudinaryField

# Custom User Model
class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('manager', 'Manager'),
        ('employee', 'Employee'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='employee')
    otp = models.CharField(max_length=6, blank=True, null=True) 
    
class Department(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='employee')
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    designation = models.CharField(max_length=100)
    date_of_joining = models.DateField()
    phone = models.CharField(max_length=15)
    address = models.TextField()
    profile_image = CloudinaryField('profile_images', null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.department}"
