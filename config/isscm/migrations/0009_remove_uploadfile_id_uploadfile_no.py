# Generated by Django 4.0.4 on 2022-04-20 13:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('isscm', '0008_alter_estimatesheet_business_number'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='uploadfile',
            name='id',
        ),
        migrations.AddField(
            model_name='uploadfile',
            name='no',
            field=models.BigAutoField(auto_created=True, default='', primary_key=True, serialize=False, verbose_name='no'),
        ),
    ]
