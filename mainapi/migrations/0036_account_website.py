# Generated by Django 3.0.8 on 2020-09-27 19:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapi', '0035_auto_20200831_2340'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='website',
            field=models.TextField(null=True),
        ),
    ]
