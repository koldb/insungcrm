# Generated by Django 4.0.4 on 2022-04-21 08:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('isscm', '0013_uploadfile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='uploadfile',
            name='uploadedFile',
            field=models.FileField(blank=True, upload_to='Uploaded Files/'),
        ),
    ]
