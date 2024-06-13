# Generated by Django 5.0.6 on 2024-06-09 20:28

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Storage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=15)),
                ('amount', models.IntegerField()),
            ],
        ),
        migrations.AlterField(
            model_name='customeraccount',
            name='first_name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='customeraccount',
            name='last_name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='customeraccount',
            name='password',
            field=models.CharField(max_length=255, validators=[django.core.validators.RegexValidator('^[0-9a-zA-Z ]+$')]),
        ),
        migrations.AlterField(
            model_name='customeraccount',
            name='user',
            field=models.CharField(max_length=255),
        ),
    ]