# Generated by Django 5.0.6 on 2024-07-03 18:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0005_alter_product_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='bread',
            field=models.PositiveIntegerField(default=0, verbose_name='نان'),
        ),
        migrations.AddField(
            model_name='product',
            name='egg',
            field=models.PositiveIntegerField(default=0, verbose_name='تخم مرغ'),
        ),
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.CharField(choices=[('hot_drinks', 'نوشیدنی گرم'), ('cold_drinks', 'نوشیدنی سرد'), ('cakes', 'کیک'), ('breakfast', 'صبحانه')], default='hot_drinks', max_length=20, verbose_name='دسته بندی محصول'),
        ),
    ]