# Generated by Django 5.1.5 on 2025-01-30 20:22

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0001_initial'),
        ('user', '0008_alter_employee_profile_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='department',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.department'),
        ),
    ]
