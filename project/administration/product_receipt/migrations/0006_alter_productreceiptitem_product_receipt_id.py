# Generated by Django 4.0.2 on 2022-04-28 20:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product_receipt', '0005_alter_productreceiptitem_product_receipt_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productreceiptitem',
            name='product_receipt_id',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='product_receipt.productreceipt'),
            preserve_default=False,
        ),
    ]
