# Generated by Django 4.1.5 on 2023-08-12 19:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('glamourApp', '0004_product_sizes'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='images',
            field=models.ManyToManyField(related_name='products', to='glamourApp.productimage'),
        ),
    ]
