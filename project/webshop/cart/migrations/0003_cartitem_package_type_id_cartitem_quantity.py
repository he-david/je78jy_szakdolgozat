# Generated by Django 4.0.2 on 2022-02-24 11:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0001_initial'),
        ('cart', '0002_cartitem'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartitem',
            name='package_type_id',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='product.packagetype'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='cartitem',
            name='quantity',
            field=models.IntegerField(default=10),
            preserve_default=False,
        ),
    ]
