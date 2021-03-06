# Generated by Django 2.2.12 on 2020-04-10 10:54

from django.db import migrations, models
import django.db.models.deletion
import modelcluster.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('wagtaildocs', '0010_document_file_hash'),
        ('topic_page', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='OfficialDocumentPage',
            fields=[
                ('janisbasepagewithtopics_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='topic_page.JanisBasePageWithTopics')),
                ('description', models.TextField(blank=True)),
                ('description_ar', models.TextField(blank=True, null=True)),
                ('description_en', models.TextField(blank=True, null=True)),
                ('description_es', models.TextField(blank=True, null=True)),
                ('description_vi', models.TextField(blank=True, null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('topic_page.janisbasepagewithtopics',),
        ),
        migrations.CreateModel(
            name='OfficialDocumentPageDocument',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sort_order', models.IntegerField(blank=True, editable=False, null=True)),
                ('date', models.DateField(null=True, verbose_name='Document date')),
                ('title', models.CharField(max_length=255, verbose_name='Document title')),
                ('title_ar', models.CharField(max_length=255, null=True, verbose_name='Document title')),
                ('title_en', models.CharField(max_length=255, null=True, verbose_name='Document title')),
                ('title_es', models.CharField(max_length=255, null=True, verbose_name='Document title')),
                ('title_vi', models.CharField(max_length=255, null=True, verbose_name='Document title')),
                ('authoring_office', models.CharField(max_length=255, verbose_name='Authoring office of document')),
                ('authoring_office_ar', models.CharField(max_length=255, null=True, verbose_name='Authoring office of document')),
                ('authoring_office_en', models.CharField(max_length=255, null=True, verbose_name='Authoring office of document')),
                ('authoring_office_es', models.CharField(max_length=255, null=True, verbose_name='Authoring office of document')),
                ('authoring_office_vi', models.CharField(max_length=255, null=True, verbose_name='Authoring office of document')),
                ('summary', models.TextField(verbose_name='Document summary')),
                ('summary_ar', models.TextField(null=True, verbose_name='Document summary')),
                ('summary_en', models.TextField(null=True, verbose_name='Document summary')),
                ('summary_es', models.TextField(null=True, verbose_name='Document summary')),
                ('summary_vi', models.TextField(null=True, verbose_name='Document summary')),
                ('name', models.CharField(max_length=255, verbose_name='Name of Document')),
                ('name_ar', models.CharField(max_length=255, null=True, verbose_name='Name of Document')),
                ('name_en', models.CharField(max_length=255, null=True, verbose_name='Name of Document')),
                ('name_es', models.CharField(max_length=255, null=True, verbose_name='Name of Document')),
                ('name_vi', models.CharField(max_length=255, null=True, verbose_name='Name of Document')),
                ('document', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtaildocs.Document', verbose_name='Document [en]')),
                ('document_es', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtaildocs.Document', verbose_name='Document [es]')),
                ('page', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='documents', to='official_documents_page.OfficialDocumentPage')),
            ],
        ),
        migrations.AddIndex(
            model_name='officialdocumentpagedocument',
            index=models.Index(fields=['-date'], name='official_do_date_51917f_idx'),
        ),
    ]
