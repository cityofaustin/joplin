# Generated by Django 2.2.9 on 2020-01-08 22:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0003_auto_20191206_0602'),
    ]

    operations = [
        migrations.AddField(
            model_name='locationpage',
            name='hours_exceptions_ar',
            field=models.TextField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='locationpage',
            name='hours_exceptions_en',
            field=models.TextField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='locationpage',
            name='hours_exceptions_es',
            field=models.TextField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='locationpage',
            name='hours_exceptions_vi',
            field=models.TextField(blank=True, max_length=255, null=True),
        ),
    ]
