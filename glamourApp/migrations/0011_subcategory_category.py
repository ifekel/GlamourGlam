# Generated by Django 4.1.5 on 2023-08-13 20:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('glamourApp', '0010_remove_productcolor_product_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='subcategory',
            name='category',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='subcategories', to='glamourApp.category'),
        ),
    ]
