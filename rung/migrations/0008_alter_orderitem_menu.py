# Generated by Django 4.2 on 2023-11-02 15:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rung', '0007_order_mail_sent'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitem',
            name='menu',
            field=models.CharField(max_length=200),
        ),
    ]
