# Generated by Django 2.2.3 on 2019-07-10 18:45

from django.db import migrations, models
import django.db.models.deletion
import modelcluster.fields
import wagtail.core.blocks
import wagtail.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0075_auto_20190627_0829'),
    ]

    operations = [
        migrations.AlterField(
            model_name='servicepage',
            name='steps',
            field=wagtail.core.fields.StreamField([('basic_step', wagtail.core.blocks.RichTextBlock(features=['ul', 'ol', 'link', 'code'], label='Basic Step')), ('step_with_options_accordian', wagtail.core.blocks.StructBlock([('options_description', wagtail.core.blocks.TextBlock('Describe the set of options')), ('options', wagtail.core.blocks.ListBlock(wagtail.core.blocks.StructBlock([('option_name', wagtail.core.blocks.TextBlock(label='Option name. (When clicked, this name will expand the content for this option')), ('option_description', wagtail.core.blocks.RichTextBlock(features=['ul', 'ol', 'link', 'code'], label='Option Content'))])))], label='Step With Options'))], blank=True, help_text='A step may have a basic text step or an options accordion which reveals two or more options', verbose_name='Write out the steps a resident needs to take to use the service'),
        ),
        migrations.AlterField(
            model_name='servicepage',
            name='steps_ar',
            field=wagtail.core.fields.StreamField([('basic_step', wagtail.core.blocks.RichTextBlock(features=['ul', 'ol', 'link', 'code'], label='Basic Step')), ('step_with_options_accordian', wagtail.core.blocks.StructBlock([('options_description', wagtail.core.blocks.TextBlock('Describe the set of options')), ('options', wagtail.core.blocks.ListBlock(wagtail.core.blocks.StructBlock([('option_name', wagtail.core.blocks.TextBlock(label='Option name. (When clicked, this name will expand the content for this option')), ('option_description', wagtail.core.blocks.RichTextBlock(features=['ul', 'ol', 'link', 'code'], label='Option Content'))])))], label='Step With Options'))], blank=True, help_text='A step may have a basic text step or an options accordion which reveals two or more options', null=True, verbose_name='Write out the steps a resident needs to take to use the service'),
        ),
        migrations.AlterField(
            model_name='servicepage',
            name='steps_en',
            field=wagtail.core.fields.StreamField([('basic_step', wagtail.core.blocks.RichTextBlock(features=['ul', 'ol', 'link', 'code'], label='Basic Step')), ('step_with_options_accordian', wagtail.core.blocks.StructBlock([('options_description', wagtail.core.blocks.TextBlock('Describe the set of options')), ('options', wagtail.core.blocks.ListBlock(wagtail.core.blocks.StructBlock([('option_name', wagtail.core.blocks.TextBlock(label='Option name. (When clicked, this name will expand the content for this option')), ('option_description', wagtail.core.blocks.RichTextBlock(features=['ul', 'ol', 'link', 'code'], label='Option Content'))])))], label='Step With Options'))], blank=True, help_text='A step may have a basic text step or an options accordion which reveals two or more options', null=True, verbose_name='Write out the steps a resident needs to take to use the service'),
        ),
        migrations.AlterField(
            model_name='servicepage',
            name='steps_es',
            field=wagtail.core.fields.StreamField([('basic_step', wagtail.core.blocks.RichTextBlock(features=['ul', 'ol', 'link', 'code'], label='Basic Step')), ('step_with_options_accordian', wagtail.core.blocks.StructBlock([('options_description', wagtail.core.blocks.TextBlock('Describe the set of options')), ('options', wagtail.core.blocks.ListBlock(wagtail.core.blocks.StructBlock([('option_name', wagtail.core.blocks.TextBlock(label='Option name. (When clicked, this name will expand the content for this option')), ('option_description', wagtail.core.blocks.RichTextBlock(features=['ul', 'ol', 'link', 'code'], label='Option Content'))])))], label='Step With Options'))], blank=True, help_text='A step may have a basic text step or an options accordion which reveals two or more options', null=True, verbose_name='Write out the steps a resident needs to take to use the service'),
        ),
        migrations.AlterField(
            model_name='servicepage',
            name='steps_vi',
            field=wagtail.core.fields.StreamField([('basic_step', wagtail.core.blocks.RichTextBlock(features=['ul', 'ol', 'link', 'code'], label='Basic Step')), ('step_with_options_accordian', wagtail.core.blocks.StructBlock([('options_description', wagtail.core.blocks.TextBlock('Describe the set of options')), ('options', wagtail.core.blocks.ListBlock(wagtail.core.blocks.StructBlock([('option_name', wagtail.core.blocks.TextBlock(label='Option name. (When clicked, this name will expand the content for this option')), ('option_description', wagtail.core.blocks.RichTextBlock(features=['ul', 'ol', 'link', 'code'], label='Option Content'))])))], label='Step With Options'))], blank=True, help_text='A step may have a basic text step or an options accordion which reveals two or more options', null=True, verbose_name='Write out the steps a resident needs to take to use the service'),
        ),
        migrations.CreateModel(
            name='ServicePageDepartments',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('departments', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='+', to='base.DepartmentPage')),
                ('page', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='related_departments', to='base.ServicePage')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
