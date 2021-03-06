# Generated by Django 4.0.2 on 2022-03-24 06:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('product', '0004_remove_category_level'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductReceipt',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('document_number_key', models.PositiveIntegerField(blank=True, null=True)),
                ('document_number', models.CharField(blank=True, max_length=20, null=True)),
                ('finalization_date', models.DateField()),
                ('status', models.CharField(choices=[('in_progress', 'Folyamatban'), ('final', 'Végleges')], max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='ProductReceiptItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('original_name', models.CharField(max_length=100)),
                ('original_package_type', models.CharField(max_length=100)),
                ('quantity', models.IntegerField()),
                ('sum_quantity', models.IntegerField()),
                ('package_type_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='product.packagetype')),
                ('product_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='product.product')),
                ('product_receipt_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product_receipt.productreceipt')),
            ],
        ),
    ]
