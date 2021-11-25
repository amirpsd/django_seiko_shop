# Generated by Django 3.2.5 on 2021-11-25 18:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='FavoriteBlog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('blogs', models.ManyToManyField(related_name='blog_favoritblog', to='blog.Blog')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='user_favoriteblogs', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'مقاله مورد علاقه',
                'verbose_name_plural': 'مقالات مورد علاقه',
            },
        ),
    ]
