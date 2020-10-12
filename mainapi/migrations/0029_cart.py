# Generated by Django 3.0.8 on 2020-08-14 14:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mainapi', '0028_account_rate_count'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('rents', models.ManyToManyField(blank=True, to='mainapi.Rent')),
                ('submit_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapi.Account')),
            ],
            options={
                'ordering': ['-created'],
            },
        ),
    ]