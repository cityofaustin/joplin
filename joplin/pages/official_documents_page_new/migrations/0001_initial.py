# Generated by Django 2.2.13 on 2020-07-02 21:14

from django.db import migrations, models
import django.db.models.deletion
import modelcluster.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('base_page', '0003_add_publish_fields'),
        ('wagtaildocs', '0010_document_file_hash'),
        ('official_documents_collection', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='OfficialDocumentPageNew',
            fields=[
                ('janisbasepage_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='base_page.JanisBasePage')),
                ('date', models.DateField(blank=True, null=True, verbose_name='Document date')),
                ('authoring_office', models.CharField(blank=True, max_length=255, verbose_name='Authoring office of document')),
                ('authoring_office_ar', models.CharField(blank=True, max_length=255, null=True, verbose_name='Authoring office of document')),
                ('authoring_office_en', models.CharField(blank=True, max_length=255, null=True, verbose_name='Authoring office of document')),
                ('authoring_office_es', models.CharField(blank=True, max_length=255, null=True, verbose_name='Authoring office of document')),
                ('authoring_office_vi', models.CharField(blank=True, max_length=255, null=True, verbose_name='Authoring office of document')),
                ('summary', models.TextField(blank=True, verbose_name='Document summary')),
                ('summary_ar', models.TextField(blank=True, null=True, verbose_name='Document summary')),
                ('summary_en', models.TextField(blank=True, null=True, verbose_name='Document summary')),
                ('summary_es', models.TextField(blank=True, null=True, verbose_name='Document summary')),
                ('summary_vi', models.TextField(blank=True, null=True, verbose_name='Document summary')),
                ('name', models.CharField(blank=True, max_length=255, verbose_name='Name of Document')),
                ('name_ar', models.CharField(blank=True, max_length=255, null=True, verbose_name='Name of Document')),
                ('name_en', models.CharField(blank=True, max_length=255, null=True, verbose_name='Name of Document')),
                ('name_es', models.CharField(blank=True, max_length=255, null=True, verbose_name='Name of Document')),
                ('name_vi', models.CharField(blank=True, max_length=255, null=True, verbose_name='Name of Document')),
                ('document', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtaildocs.Document', verbose_name='Document [en]')),
                ('document_es', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtaildocs.Document', verbose_name='Document [es]')),
            ],
            options={
                'abstract': False,
            },
            bases=('base_page.janisbasepage',),
        ),
        migrations.CreateModel(
            name='OfficialDocumentCollectionDocument',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('official_document_collection', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='official_documents_collection.OfficialDocumentCollection', verbose_name='Select an Official Document Collection')),
                ('page', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='official_document_collection', to='official_documents_page_new.OfficialDocumentPageNew')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
