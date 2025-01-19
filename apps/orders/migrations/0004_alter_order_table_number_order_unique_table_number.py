# Generated by Django 5.1.5 on 2025-01-18 12:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_remove_order_allowable_status_values_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='table_number',
            field=models.IntegerField(),
        ),
        migrations.AddConstraint(
            model_name='order',
            constraint=models.UniqueConstraint(fields=('table_number',), name='unique_table_number', violation_error_message='Номер стола уже занят'),
        ),
    ]
