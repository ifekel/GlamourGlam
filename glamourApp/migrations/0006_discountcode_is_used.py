# Generated by Django 4.1.5 on 2023-08-27 15:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('glamourApp', '0005_delete_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='discountcode',
            name='is_used',
            field=models.BooleanField(default=False),
        ),
    ]
