# Generated by Django 4.1.5 on 2023-08-13 05:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('glamourApp', '0005_product_images'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='sizes',
            field=models.ManyToManyField(blank=True, null=True, related_name='products', to='glamourApp.productsize'),
        ),
    ]
