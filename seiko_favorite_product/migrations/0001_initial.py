# Generated by Django 3.2.5 on 2021-09-28 01:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('seiko_shop', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='FavoriteProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('products', models.ManyToManyField(default=None, related_name='products_favorite_product', to='seiko_shop.Product')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='user_favorite_product', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'محصول مورد علاقه',
                'verbose_name_plural': 'محصولات مورد علاقه',
            },
        ),
    ]
