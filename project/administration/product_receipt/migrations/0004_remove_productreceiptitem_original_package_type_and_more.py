# Generated by Django 4.0.2 on 2022-03-24 09:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product_receipt', '0003_productreceipt_sum_quantity'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productreceiptitem',
            name='original_package_type',
        ),
        migrations.RemoveField(
            model_name='productreceiptitem',
            name='package_type_id',
        ),
        migrations.RemoveField(
            model_name='productreceiptitem',
            name='sum_quantity',
        ),
    ]