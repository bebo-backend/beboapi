# Generated by Django 3.0.8 on 2020-08-14 13:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapi', '0027_auto_20200814_0500'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='rate_count',
            field=models.IntegerField(default=0, null=True),
        ),
    ]
