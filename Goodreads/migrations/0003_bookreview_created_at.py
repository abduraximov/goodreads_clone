# Generated by Django 4.0 on 2023-04-13 20:01

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('Goodreads', '0002_book_cover_picture'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookreview',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
