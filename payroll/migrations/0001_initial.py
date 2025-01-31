# Generated by Django 5.1.5 on 2025-01-31 10:20

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user', '0008_alter_employee_profile_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payroll',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('basic_salary', models.DecimalField(decimal_places=2, max_digits=10)),
                ('bonus', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('deductions', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('tax', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('employee', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='payroll', to='user.employee')),
            ],
        ),
        migrations.CreateModel(
            name='Payslip',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('month', models.CharField(choices=[('January', 'January'), ('February', 'February'), ('March', 'March'), ('April', 'April'), ('May', 'May'), ('June', 'June'), ('July', 'July'), ('August', 'August'), ('September', 'September'), ('October', 'October'), ('November', 'November'), ('December', 'December')], max_length=20)),
                ('year', models.IntegerField(default=2025)),
                ('basic_salary', models.DecimalField(decimal_places=2, max_digits=10)),
                ('bonus', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('deductions', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('tax', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('net_salary', models.DecimalField(decimal_places=2, max_digits=10)),
                ('paid', models.BooleanField(default=False)),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payslips', to='user.employee')),
            ],
        ),
    ]
