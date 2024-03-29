# Generated by Django 4.2.6 on 2024-01-10 15:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rung', '0018_shop_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shop_time',
            name='shop_closing_time',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='shop_time',
            name='shop_delivery_closing_time',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='shop_time',
            name='shop_delivery_opening_time',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='shop_time',
            name='shop_opening_time',
            field=models.TimeField(blank=True, null=True),
        ),
    ]
