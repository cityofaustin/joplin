# Generated by Django 2.2.14 on 2020-08-13 20:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('official_documents_page', '0007_auto_20200807_1819'),
    ]

    operations = [
        migrations.AlterField(
            model_name='officialdocumentpage',
            name='body',
            field=models.TextField(blank=True, verbose_name='Document text'),
        ),
        migrations.AlterField(
            model_name='officialdocumentpage',
            name='body_ar',
            field=models.TextField(blank=True, null=True, verbose_name='Document text'),
        ),
        migrations.AlterField(
            model_name='officialdocumentpage',
            name='body_en',
            field=models.TextField(blank=True, null=True, verbose_name='Document text'),
        ),
        migrations.AlterField(
            model_name='officialdocumentpage',
            name='body_es',
            field=models.TextField(blank=True, null=True, verbose_name='Document text'),
        ),
        migrations.AlterField(
            model_name='officialdocumentpage',
            name='body_vi',
            field=models.TextField(blank=True, null=True, verbose_name='Document text'),
        ),
    ]
