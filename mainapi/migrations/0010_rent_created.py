# Generated by Django 3.0.8 on 2020-07-24 10:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapi', '0009_auto_20200723_0200'),
    ]

    operations = [
        migrations.AddField(
            model_name='rent',
            name='created',
            field=models.DateTimeField(auto_now=True),
        ),
    ]