# Generated by Django 5.1.5 on 2025-01-24 08:56

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='PerformanceReview',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('review_date', models.DateField(auto_now_add=True)),
                ('period_start', models.DateField()),
                ('period_end', models.DateField()),
                ('feedback', models.TextField()),
                ('rating', models.DecimalField(decimal_places=2, help_text='Rating out of 10', max_digits=4)),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='performance_reviews', to=settings.AUTH_USER_MODEL)),
                ('reviewer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='given_reviews', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-review_date'],
            },
        ),
    ]
