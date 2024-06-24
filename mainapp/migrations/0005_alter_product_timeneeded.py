# Generated by Django 5.0.6 on 2024-06-24 22:00

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0004_alter_product_chocolate_alter_product_coffee_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='timeNeeded',
            field=models.IntegerField(default=0, validators=[django.core.validators.MaxValueValidator(60)], verbose_name='زمان مورد نیاز'),
        ),
    ]
