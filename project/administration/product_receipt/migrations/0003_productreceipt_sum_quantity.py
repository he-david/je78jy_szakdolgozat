# Generated by Django 4.0.2 on 2022-03-24 07:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product_receipt', '0002_alter_productreceipt_finalization_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='productreceipt',
            name='sum_quantity',
            field=models.IntegerField(default=0),
        ),
    ]
