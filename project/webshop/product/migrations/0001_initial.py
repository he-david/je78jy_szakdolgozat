# Generated by Django 4.0.2 on 2022-02-23 11:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Action',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('from_date', models.DateField()),
                ('to_date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('parent_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='product.category')),
            ],
            options={
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='PackageType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('summary_name', models.CharField(max_length=50)),
                ('display_name', models.CharField(max_length=50)),
                ('quantity', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('producer', models.CharField(max_length=100)),
                ('net_price', models.IntegerField(default=0)),
                ('vat', models.IntegerField()),
                ('description', models.TextField(blank=True, null=True)),
                ('free_stock', models.IntegerField(default=0)),
                ('reserved_stock', models.IntegerField(default=0)),
                ('image', models.ImageField(blank=True, null=True, upload_to='product_images')),
                ('slug', models.SlugField(unique=True)),
                ('action_id', models.ManyToManyField(blank=True, to='product.Action')),
                ('category_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='product.category')),
                ('package_type_id', models.ManyToManyField(to='product.PackageType')),
            ],
        ),
    ]
