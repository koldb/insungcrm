# Generated by Django 4.0.4 on 2022-04-21 13:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('isscm', '0017_alter_estimatesheet_rp_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='estimatesheet',
            name='sheet_no',
            field=models.IntegerField(null=True),
        ),
    ]
