# Generated by Django 3.0.8 on 2020-08-10 04:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mainapi', '0019_rent_rate'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reviews',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapi.Account')),
            ],
        ),
        migrations.AddField(
            model_name='rent',
            name='reviews',
            field=models.ManyToManyField(to='mainapi.Reviews'),
        ),
    ]
