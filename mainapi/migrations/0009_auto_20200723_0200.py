# Generated by Django 3.0.8 on 2020-07-23 02:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainapi', '0008_auto_20200723_0053'),
    ]

    operations = [
        migrations.RenameField(
            model_name='account',
            old_name='location',
            new_name='agencyname',
        ),
    ]
