# Generated by Django 5.1 on 2024-12-10 18:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tags', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='tag',
            name='slug',
            field=models.SlugField(default='default', unique=True),
            preserve_default=False,
        ),
    ]