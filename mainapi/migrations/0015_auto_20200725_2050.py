# Generated by Django 3.0.8 on 2020-07-25 20:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapi', '0014_auto_20200725_2049'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rent',
            name='created',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
