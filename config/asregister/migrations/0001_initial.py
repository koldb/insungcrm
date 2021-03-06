# Generated by Django 4.0.4 on 2022-06-02 15:36

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import isscm.utils


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ASsheet',
            fields=[
                ('no', models.AutoField(primary_key=True, serialize=False)),
                ('cname', models.CharField(blank=True, max_length=100, null=True, verbose_name='업체명')),
                ('cuser', models.CharField(blank=True, max_length=20, null=True, verbose_name='성함')),
                ('cphone', models.CharField(blank=True, max_length=30, null=True, unique=True, validators=[django.core.validators.RegexValidator(regex='\\d{2,3}-\\d{3,4}-\\d{4}')], verbose_name='연락처')),
                ('rg_date', models.DateTimeField(auto_now_add=True, verbose_name='고객 접수일')),
                ('rp_date', models.DateField(blank=True, max_length=50, null=True, verbose_name='마감 요청일')),
                ('end_date', models.DateField(blank=True, max_length=50, null=True, verbose_name='종료일자')),
                ('product_name', models.CharField(max_length=100, verbose_name='제품 이름')),
                ('quantity', models.IntegerField(blank=True, default=0, null=True)),
                ('serial', models.CharField(blank=True, max_length=20, null=True, verbose_name='시리얼')),
                ('site', models.CharField(blank=True, max_length=20, null=True, verbose_name='현장명')),
                ('symptom', models.CharField(blank=True, max_length=200, null=True, verbose_name='증상')),
                ('memo', models.TextField(blank=True, null=True, verbose_name='비고')),
                ('option', models.TextField(blank=True, null=True, verbose_name='의견')),
                ('finish', models.CharField(blank=True, max_length=10, null=True, verbose_name='완료 여부')),
            ],
            options={
                'verbose_name': 'AS접수',
                'verbose_name_plural': 'AS접수',
                'db_table': 'assheet',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='ASUploadFile',
            fields=[
                ('no', models.AutoField(primary_key=True, serialize=False)),
                ('cname', models.CharField(max_length=100, null=True)),
                ('title', models.CharField(max_length=200, null=True)),
                ('uploadedFile', models.FileField(blank=True, upload_to=isscm.utils.rename_file_to_uuid)),
                ('dateTimeOfUpload', models.DateTimeField(auto_now=True)),
                ('menu', models.TextField(blank=True, null=True)),
                ('sheet_no', models.ForeignKey(db_column='sheet_no', null=True, on_delete=django.db.models.deletion.CASCADE, to='asregister.assheet')),
            ],
            options={
                'verbose_name': 'AS file 업로드',
                'verbose_name_plural': 'AS file 업로드',
                'db_table': 'ASuploadfile',
                'managed': True,
            },
        ),
    ]
