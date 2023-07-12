# Generated by Django 4.2.2 on 2023-07-04 11:05

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('goals', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='goal',
            name='deadline',
        ),
        migrations.AddField(
            model_name='goal',
            name='due_date',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Дата выполнения'),
        ),
        migrations.AlterField(
            model_name='goal',
            name='description',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Описание'),
        ),
        migrations.AlterField(
            model_name='goal',
            name='title',
            field=models.CharField(max_length=255, validators=[django.core.validators.MinLengthValidator(1)], verbose_name='Заголовок'),
        ),
        migrations.AlterField(
            model_name='goalcomment',
            name='text',
            field=models.CharField(validators=[django.core.validators.MinLengthValidator(1)], verbose_name='Текст'),
        ),
    ]