# Generated by Django 3.0.8 on 2020-08-31 23:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapi', '0034_auto_20200828_0726'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rent',
            name='instock',
            field=models.CharField(default=1, max_length=20, null=True),
        ),
    ]
