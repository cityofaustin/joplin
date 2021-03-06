# Generated by Django 2.2.13 on 2020-07-08 01:26

from django.db import migrations, models
import django.db.models.deletion
import modelcluster.fields


class Migration(migrations.Migration):

    dependencies = [
        ('official_documents_collection', '0001_initial'),
        ('official_documents_page', '0003_officialdocumentpage'),
    ]

    operations = [
        migrations.CreateModel(
            name='OfficialDocumentCollectionDocument',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('official_document_collection', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='official_documents_collection.OfficialDocumentCollection', verbose_name='Select an Official Document Collection')),
                ('page', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='official_document_collection', to='official_documents_page.OfficialDocumentPage')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
