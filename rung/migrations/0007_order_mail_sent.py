# Generated by Django 4.2 on 2023-10-31 13:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rung', '0006_alter_order_delivery_option'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='mail_sent',
            field=models.BooleanField(default=False),
        ),
    ]
