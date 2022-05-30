# Generated by Django 4.0.4 on 2022-05-30 16:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('isscm', '0004_alter_sub_sheet_m_title'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='uploadfile',
            name='sheet_no',
        ),
        migrations.AddField(
            model_name='uploadfile',
            name='main_id',
            field=models.ForeignKey(db_column='main_id', null=True, on_delete=django.db.models.deletion.CASCADE, to='isscm.main_sheet'),
        ),
    ]
