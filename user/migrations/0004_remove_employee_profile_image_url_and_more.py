# Generated by Django 5.1.5 on 2025-01-29 10:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_alter_employee_profile_image_url'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='employee',
            name='profile_image_url',
        ),
        migrations.AddField(
            model_name='employee',
            name='profile_image',
            field=models.ImageField(blank=True, null=True, upload_to='profile_images'),
        ),
    ]
