# Generated by Django 3.0.8 on 2020-07-25 15:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapi', '0011_auto_20200725_1454'),
    ]

    operations = [
        migrations.AddField(
            model_name='rent',
            name='category',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='rent',
            name='title',
            field=models.CharField(max_length=120, null=True),
        ),
    ]
