# Generated by Django 3.2.5 on 2022-02-24 01:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('product', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=150, verbose_name='full name')),
                ('city', models.CharField(max_length=100, verbose_name='city')),
                ('address', models.CharField(max_length=250, verbose_name='address')),
                ('postal_code', models.CharField(max_length=20, verbose_name='postal_code')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('paid', models.BooleanField(default=False, verbose_name='is paid?')),
                ('discount', models.IntegerField(blank=True, default=None, null=True, verbose_name='discount')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to=settings.AUTH_USER_MODEL, verbose_name='کاربر')),
            ],
            options={
                'verbose_name': 'order',
                'verbose_name_plural': 'orders',
                'ordering': ('-created',),
            },
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.IntegerField(verbose_name='price')),
                ('quantity', models.PositiveSmallIntegerField(default=1, verbose_name='quantity')),
                ('color', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='product.color', verbose_name='color')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='orders.order', verbose_name='order')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_items', to='product.product', verbose_name='product')),
                ('size', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='product.size', verbose_name='size')),
            ],
            options={
                'verbose_name': 'cart',
                'verbose_name_plural': 'carts',
            },
        ),
    ]
