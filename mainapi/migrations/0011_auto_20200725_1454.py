# Generated by Django 3.0.8 on 2020-07-25 14:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapi', '0010_rent_created'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='created',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='rent',
            name='created',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
