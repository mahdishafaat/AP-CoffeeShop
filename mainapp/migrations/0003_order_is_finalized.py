# Generated by Django 5.0.6 on 2024-07-03 12:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0002_alter_order_order_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='is_finalized',
            field=models.BooleanField(default=False),
        ),
    ]