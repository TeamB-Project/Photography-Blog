# Generated by Django 4.0.3 on 2022-05-11 22:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('photos', '0009_photocategory_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='photo',
            name='camera',
            field=models.CharField(blank=True, max_length=80, null=True),
        ),
        migrations.AddField(
            model_name='photo',
            name='focal',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='photo',
            name='iso',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='photo',
            name='shutter',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]