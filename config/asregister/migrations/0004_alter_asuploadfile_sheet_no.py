# Generated by Django 4.0.4 on 2022-05-09 17:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('asregister', '0003_asuploadfile_menu'),
    ]

    operations = [
        migrations.AlterField(
            model_name='asuploadfile',
            name='sheet_no',
            field=models.ForeignKey(db_column='sheet_no', null=True, on_delete=django.db.models.deletion.CASCADE, to='asregister.assheet'),
        ),
    ]