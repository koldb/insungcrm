# Generated by Django 4.0.4 on 2022-04-19 17:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('isscm', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='estimatesheet',
            name='file_name',
        ),
        migrations.RemoveField(
            model_name='estimatesheet',
            name='memo',
        ),
    ]
