# Generated by Django 4.2 on 2023-11-02 15:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rung', '0008_alter_orderitem_menu'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='cost',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='order',
            name='total_price',
            field=models.FloatField(default=0),
        ),
    ]