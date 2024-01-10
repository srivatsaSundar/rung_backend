# Generated by Django 4.2.6 on 2024-01-10 13:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rung', '0017_discount_coupon_available'),
    ]

    operations = [
        migrations.CreateModel(
            name='shop_time',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('shop_opening_time', models.TextField(blank=True, null=True)),
                ('shop_closing_time', models.TextField(blank=True, null=True)),
                ('shop_delivery_opening_time', models.TextField(blank=True, null=True)),
                ('shop_delivery_closing_time', models.TextField(blank=True, null=True)),
            ],
        ),
    ]
