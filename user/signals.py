from django.db.models.signals import post_delete
from django.dispatch import receiver
from .models import Employee

@receiver(post_delete, sender=Employee)
def delete_user_when_employee_deleted(sender, instance, **kwargs):
    if instance.user:
        instance.user.delete()
