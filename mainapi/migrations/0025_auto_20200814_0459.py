# Generated by Django 3.0.8 on 2020-08-14 04:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapi', '0024_auto_20200814_0458'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rent',
            name='reviews',
            field=models.ManyToManyField(null=True, to='mainapi.Reviews'),
        ),
    ]
