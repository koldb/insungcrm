# Generated by Django 4.0.4 on 2022-05-04 15:52

from django.db import migrations, models
import isscm.utils


class Migration(migrations.Migration):

    dependencies = [
        ('isscm', '0002_alter_orderuploadfile_uploadedfile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='uploadfile',
            name='uploadedFile',
            field=models.FileField(blank=True, upload_to=isscm.utils.rename_file_to_uuid),
        ),
    ]
