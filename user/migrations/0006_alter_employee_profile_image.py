# Generated by Django 5.1.5 on 2025-01-29 14:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0005_remove_employee_password'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='profile_image',
            field=models.FileField(blank=True, null=True, upload_to='profile_images'),
        ),
    ]
