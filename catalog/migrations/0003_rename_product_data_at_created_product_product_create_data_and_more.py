# Generated by Django 4.2.6 on 2023-10-19 10:05

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0002_product_product_data_at_created'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='product_data_at_created',
            new_name='product_create_data',
        ),
        migrations.RemoveField(
            model_name='product',
            name='product_data_created',
        ),
        migrations.RemoveField(
            model_name='product',
            name='product_last_data_change',
        ),
        migrations.AddField(
            model_name='category',
            name='create_at',
            field=models.DateField(default=datetime.date.today, verbose_name='на удаление'),
        ),
    ]