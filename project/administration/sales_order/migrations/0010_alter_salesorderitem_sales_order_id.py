# Generated by Django 4.0.2 on 2022-04-09 13:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sales_order', '0009_remove_salesorderitem_original_unit_quantity_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='salesorderitem',
            name='sales_order_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='sales_order.salesorder'),
        ),
    ]