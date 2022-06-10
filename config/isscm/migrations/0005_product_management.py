# Generated by Django 4.0.4 on 2022-06-10 13:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('isscm', '0004_notice'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product_Management',
            fields=[
                ('no', models.AutoField(primary_key=True, serialize=False)),
                ('rg_date', models.DateTimeField(auto_now_add=True, verbose_name='등록일자')),
                ('product_name', models.CharField(blank=True, max_length=50, null=True, verbose_name='제품명')),
                ('serial', models.CharField(blank=True, max_length=20, null=True, verbose_name='시리얼')),
                ('current_location', models.CharField(blank=True, max_length=30, null=True, verbose_name='현재 위치')),
                ('status', models.CharField(blank=True, max_length=10, null=True, verbose_name='상태')),
            ],
            options={
                'verbose_name': '제품관리',
                'verbose_name_plural': '제품관리',
                'db_table': 'product_management',
                'managed': True,
            },
        ),
    ]