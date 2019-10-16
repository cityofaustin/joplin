# Generated by Django 2.2.6 on 2019-10-16 22:54

from django.db import migrations, models
import django.db.models.deletion
import modelcluster.fields


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0041_group_collection_permissions_verbose_name_plural'),
        ('base', '0092_auto_20191003_1358'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='guidepagetopic',
            name='toplink',
        ),
        migrations.RemoveField(
            model_name='informationpagetopic',
            name='toplink',
        ),
        migrations.RemoveField(
            model_name='officialdocumentpagetopic',
            name='toplink',
        ),
        migrations.RemoveField(
            model_name='servicepagetopic',
            name='toplink',
        ),
        migrations.CreateModel(
            name='TopicPageTopPage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sort_order', models.IntegerField(blank=True, editable=False, null=True)),
                ('page', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='wagtailcore.Page', verbose_name='Select a page')),
                ('topic', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='top_pages', to='base.TopicPage')),
            ],
            options={
                'ordering': ['sort_order'],
                'abstract': False,
            },
        ),
    ]
