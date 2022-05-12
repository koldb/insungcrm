# Generated by Django 4.0.4 on 2022-05-12 10:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('question', '0003_question_comment_parent_comment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question_comment',
            name='parent_comment',
            field=models.ForeignKey(db_column='parent_comment', null=True, on_delete=django.db.models.deletion.CASCADE, to='question.question_comment'),
        ),
    ]
