# Generated by Django 4.1.5 on 2023-08-20 12:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('glamourApp', '0015_rename_order_id_order_order_number_order_tracking_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='tracking_id',
        ),
        migrations.AlterField(
            model_name='shippingaddress',
            name='appartment',
            field=models.CharField(blank=True, default='None specified', max_length=200, null=True),
        ),
    ]
