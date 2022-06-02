# Generated by Django 4.0.4 on 2022-05-31 14:10

from django.db import migrations, models
import django.db.models.deletion
import isscm.utils


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='main_sheet',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('rg_date', models.DateTimeField(auto_now_add=True, verbose_name='등록일자')),
                ('rp_date', models.DateField(blank=True, max_length=50, null=True, verbose_name='마감일자')),
                ('main_title', models.CharField(blank=True, max_length=50, null=True, verbose_name='견적명')),
                ('cname', models.CharField(blank=True, max_length=100, null=True, verbose_name='업체명')),
                ('requests', models.TextField(blank=True, null=True, verbose_name='요청사항')),
                ('total_price', models.IntegerField(blank=True, default=0, null=True, verbose_name='총금액')),
                ('finish', models.CharField(blank=True, max_length=10, null=True, verbose_name='완료여부')),
                ('user_dept', models.CharField(blank=True, max_length=20, null=True, verbose_name='부서명')),
                ('user_name', models.CharField(blank=True, max_length=20, null=True, verbose_name='담당자')),
            ],
            options={
                'verbose_name': '메인',
                'verbose_name_plural': '메인',
                'db_table': 'MainSheet',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='ProductDb',
            fields=[
                ('no', models.IntegerField(auto_created=True, primary_key=True, serialize=False)),
                ('center_code', models.TextField(blank=True, null=True)),
                ('center', models.TextField(blank=True, null=True)),
                ('warehouse_code', models.TextField(blank=True, null=True)),
                ('warehouse_name', models.TextField(blank=True, null=True)),
                ('product_code', models.TextField(blank=True, null=True)),
                ('product_num', models.TextField(blank=True, null=True)),
                ('scan_code', models.TextField(blank=True, null=True)),
                ('product_name', models.TextField(blank=True, null=True)),
                ('account_code', models.TextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'product_db',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='UploadFile',
            fields=[
                ('no', models.AutoField(primary_key=True, serialize=False)),
                ('cname', models.CharField(max_length=100, null=True)),
                ('title', models.CharField(max_length=200, null=True)),
                ('uploadedFile', models.FileField(blank=True, upload_to=isscm.utils.rename_file_to_uuid)),
                ('dateTimeOfUpload', models.DateTimeField(auto_now=True)),
                ('menu', models.TextField(blank=True, null=True)),
                ('main_id', models.ForeignKey(db_column='main_id', null=True, on_delete=django.db.models.deletion.CASCADE, to='isscm.main_sheet')),
            ],
            options={
                'verbose_name': '업로드',
                'verbose_name_plural': '업로드',
                'db_table': 'uploadfile',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='sub_sheet',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('m_title', models.CharField(blank=True, max_length=100, null=True, verbose_name='메인 title')),
                ('rg_date', models.DateTimeField(auto_now_add=True, verbose_name='등록일자')),
                ('product_name', models.CharField(max_length=100, verbose_name='제품 이름')),
                ('quantity', models.IntegerField(blank=True, default=0, null=True, verbose_name='수량')),
                ('per_price', models.IntegerField(blank=True, default=0, null=True, verbose_name='단가')),
                ('tax', models.IntegerField(blank=True, default=0, null=True, verbose_name='부가세')),
                ('total_price', models.IntegerField(blank=True, default=0, null=True, verbose_name='총금액')),
                ('cname', models.CharField(blank=True, max_length=100, null=True, verbose_name='업체명')),
                ('m_id', models.ForeignKey(db_column='m_id', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='m_id', to='isscm.main_sheet')),
            ],
            options={
                'verbose_name': '서브',
                'verbose_name_plural': '서브',
                'db_table': 'SubSheet',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='product_info',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('rg_date', models.DateTimeField(auto_now_add=True, verbose_name='등록일자')),
                ('product_name', models.CharField(max_length=100, verbose_name='제품 이름')),
                ('cname', models.CharField(blank=True, max_length=100, null=True, verbose_name='업체명')),
                ('serial', models.CharField(blank=True, max_length=20, null=True, verbose_name='시리얼')),
                ('production_date', models.DateField(blank=True, null=True, verbose_name='생산일자')),
                ('release_date', models.DateField(blank=True, null=True, verbose_name='출고일자')),
                ('warranty', models.DateField(blank=True, null=True, verbose_name='보증만료일')),
                ('s_id', models.ForeignKey(db_column='s_id', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='s_id', to='isscm.sub_sheet')),
            ],
            options={
                'verbose_name': '제품정보',
                'verbose_name_plural': '제품정보',
                'db_table': 'product_info',
                'managed': True,
            },
        ),
    ]
