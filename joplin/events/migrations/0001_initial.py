# Generated by Django 2.2.9 on 2020-01-29 00:37

from django.db import migrations, models
import django.db.models.deletion
import modelcluster.fields
import wagtail.core.blocks
import wagtail.core.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('base', '0003_auto_20200107_2305'),
        ('wagtailcore', '0041_group_collection_permissions_verbose_name_plural'),
    ]

    operations = [
        migrations.CreateModel(
            name='EventPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('author_notes', wagtail.core.fields.RichTextField(blank=True, verbose_name='Notes for authors (Not visible on the resident facing site)')),
                ('coa_global', models.BooleanField(default=False, verbose_name='Make this a top level page')),
                ('description', wagtail.core.fields.RichTextField(blank=True, verbose_name='Full description of the event')),
                ('description_ar', wagtail.core.fields.RichTextField(blank=True, null=True, verbose_name='Full description of the event')),
                ('description_en', wagtail.core.fields.RichTextField(blank=True, null=True, verbose_name='Full description of the event')),
                ('description_es', wagtail.core.fields.RichTextField(blank=True, null=True, verbose_name='Full description of the event')),
                ('description_vi', wagtail.core.fields.RichTextField(blank=True, null=True, verbose_name='Full description of the event')),
                ('date', models.DateField(blank=True, null=True, verbose_name='Event date')),
                ('start_time', models.TimeField(blank=True, null=True)),
                ('end_time', models.TimeField(blank=True, null=True)),
                ('location_blocks', wagtail.core.fields.StreamField([('city_location', wagtail.core.blocks.StructBlock([('location_page', wagtail.core.blocks.PageChooserBlock(classname='do-not-hide', label='Location', page_type=['locations.LocationPage'])), ('additional_details_en', wagtail.core.blocks.TextBlock(label='Any other necessary location details, such as room number [en]', required=False)), ('additional_details_es', wagtail.core.blocks.TextBlock(label='Any other necessary location details, such as room number [es]', required=False)), ('additional_details_ar', wagtail.core.blocks.TextBlock(label='Any other necessary location details, such as room number [ar]', required=False)), ('additional_details_vi', wagtail.core.blocks.TextBlock(label='Any other necessary location details, such as room number [vi]', required=False))])), ('remote_location', wagtail.core.blocks.StructBlock([('name_en', wagtail.core.blocks.TextBlock(label='Name of venue [en]')), ('name_es', wagtail.core.blocks.TextBlock(label='Name of venue [es]', required=False)), ('name_ar', wagtail.core.blocks.TextBlock(label='Name of venue [ar]', required=False)), ('name_vi', wagtail.core.blocks.TextBlock(label='Name of venue [vi]', required=False)), ('street', wagtail.core.blocks.TextBlock(label='Street', required=False)), ('unit', wagtail.core.blocks.TextBlock(label='Unit', required=False)), ('city', wagtail.core.blocks.TextBlock(label='City', required=False)), ('state', wagtail.core.blocks.TextBlock(label='State', required=False)), ('country', wagtail.core.blocks.TextBlock(label='Country', required=False)), ('zip', wagtail.core.blocks.TextBlock(label='ZIP', required=False)), ('additional_details_en', wagtail.core.blocks.TextBlock(label='Any other necessary location details, such as room number [en]', required=False)), ('additional_details_es', wagtail.core.blocks.TextBlock(label='Any other necessary location details, such as room number [es]', required=False)), ('additional_details_ar', wagtail.core.blocks.TextBlock(label='Any other necessary location details, such as room number [ar]', required=False)), ('additional_details_vi', wagtail.core.blocks.TextBlock(label='Any other necessary location details, such as room number [vi]', required=False))]))], blank=True, verbose_name='Add location of event')),
                ('event_is_free', models.BooleanField(default=True, verbose_name='This event is free')),
                ('registration_url', models.URLField(blank=True, verbose_name='The URL where the resident may register for the event, if needed')),
                ('canceled', models.BooleanField(default=False, verbose_name='Cancel this event')),
                ('contact', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='base.Contact')),
            ],
            options={
                'permissions': [('view_extra_panels', 'Can view extra panels'), ('view_snippets', 'Can view snippets'), ('add_snippets', 'Can add snippet'), ('delete_snippets', 'Can delete snippet')],
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='EventPageRelatedDepartments',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('page', modelcluster.fields.ParentalKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='related_departments', to='events.EventPage')),
                ('related_department', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='base.DepartmentPage')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='EventPageFee',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fee', models.DecimalField(blank=True, decimal_places=2, max_digits=10)),
                ('fee_label', models.CharField(blank=True, max_length=255, verbose_name='Label (kids, adults, seniors, etc.)')),
                ('fee_label_ar', models.CharField(blank=True, max_length=255, null=True, verbose_name='Label (kids, adults, seniors, etc.)')),
                ('fee_label_en', models.CharField(blank=True, max_length=255, null=True, verbose_name='Label (kids, adults, seniors, etc.)')),
                ('fee_label_es', models.CharField(blank=True, max_length=255, null=True, verbose_name='Label (kids, adults, seniors, etc.)')),
                ('fee_label_vi', models.CharField(blank=True, max_length=255, null=True, verbose_name='Label (kids, adults, seniors, etc.)')),
                ('page', modelcluster.fields.ParentalKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='fees', to='events.EventPage')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
