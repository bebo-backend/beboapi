# Generated by Django 3.0.8 on 2020-07-25 16:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapi', '0012_auto_20200725_1546'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rent',
            name='views',
            field=models.IntegerField(default=1, null=True),
        ),
    ]