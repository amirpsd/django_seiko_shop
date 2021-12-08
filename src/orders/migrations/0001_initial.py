# Generated by Django 3.2.5 on 2021-12-08 23:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('product', '0003_alter_product_discount'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=150, verbose_name='نام و نام خانوادگی')),
                ('city', models.CharField(max_length=100, verbose_name='شهر')),
                ('address', models.CharField(max_length=250, verbose_name='آدرس')),
                ('postal_code', models.CharField(max_length=20, verbose_name='کد پستی')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('paid', models.BooleanField(default=False, verbose_name='پرداخت شده ؟')),
                ('discount', models.IntegerField(blank=True, default=None, null=True, verbose_name='تخفیف')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to=settings.AUTH_USER_MODEL, verbose_name='کاربر')),
            ],
            options={
                'verbose_name': 'سفارش',
                'verbose_name_plural': 'سفارشات',
                'ordering': ('-created',),
            },
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.IntegerField(verbose_name='قیمت')),
                ('quantity', models.PositiveSmallIntegerField(default=1, verbose_name='تعداد')),
                ('color', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='product.color', verbose_name='رنگ')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='orders.order', verbose_name='سفارش')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_items', to='product.product', verbose_name='محصول')),
                ('size', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='product.size', verbose_name='سایز')),
            ],
            options={
                'verbose_name': 'سبد خرید',
                'verbose_name_plural': 'سبد های خرید',
            },
        ),
    ]
