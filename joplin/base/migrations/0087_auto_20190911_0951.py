# Generated by Django 2.2.5 on 2019-09-11 09:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wagtaildocs', '0010_document_file_hash'),
        ('base', '0086_remove_topicpage_external_services'),
    ]

    operations = [
        migrations.AddField(
            model_name='officialdocumentpageofficialdocument',
            name='document',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtaildocs.Document'),
        ),
        migrations.AlterField(
            model_name='officialdocumentpageofficialdocument',
            name='link',
            field=models.URLField(blank=True, null=True, verbose_name='Link to Document (URL)'),
        ),
    ]
