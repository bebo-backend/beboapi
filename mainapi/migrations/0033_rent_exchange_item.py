# Generated by Django 3.0.8 on 2020-08-28 01:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapi', '0032_auto_20200822_1310'),
    ]

    operations = [
        migrations.AddField(
            model_name='rent',
            name='exchange_item',
            field=models.TextField(blank=True, null=True),
        ),
    ]
