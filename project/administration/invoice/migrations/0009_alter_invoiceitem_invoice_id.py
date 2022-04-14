# Generated by Django 4.0.2 on 2022-04-09 13:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('invoice', '0008_invoiceitem_original_package_display_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoiceitem',
            name='invoice_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='invoice.invoice'),
        ),
    ]