# Generated by Django 4.0.3 on 2022-04-26 00:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('photos', '0007_alter_photo_slug'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='photo',
            name='slug',
        ),
    ]
