# Generated by Django 4.2.6 on 2023-12-24 18:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rung', '0014_holiday_notes'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='holiday_notes',
            name='end_time',
        ),
        migrations.RemoveField(
            model_name='holiday_notes',
            name='start_time',
        ),
        migrations.AlterField(
            model_name='holiday_notes',
            name='end_data',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='holiday_notes',
            name='start_data',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
