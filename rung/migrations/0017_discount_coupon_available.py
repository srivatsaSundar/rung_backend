# Generated by Django 4.2.6 on 2024-01-07 05:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rung', '0016_countrycode_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='discount_coupon',
            name='available',
            field=models.BooleanField(default=True),
        ),
    ]