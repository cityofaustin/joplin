# Generated by Django 2.2.5 on 2019-09-13 19:27

from django.db import migrations
import wagtail.core.blocks
import wagtail.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0086_remove_topicpage_external_services'),
    ]

    operations = [
        migrations.AlterField(
            model_name='servicepage',
            name='steps',
            field=wagtail.core.fields.StreamField([('basic_step', wagtail.core.blocks.RichTextBlock(features=['ul', 'ol', 'link', 'code', 'rich-text-button-link'], label='Basic Step')), ('step_with_options_accordian', wagtail.core.blocks.StructBlock([('options_description', wagtail.core.blocks.RichTextBlock(classname='odd-placeholder odd-value_Option-description', features=['ul', 'ol', 'link', 'code', 'rich-text-button-link'])), ('options', wagtail.core.blocks.ListBlock(wagtail.core.blocks.StructBlock([('option_name', wagtail.core.blocks.TextBlock(label='Option name. (When clicked, this name will expand the content for this option')), ('option_description', wagtail.core.blocks.RichTextBlock(features=['ul', 'ol', 'link', 'code', 'rich-text-button-link'], label='Option Content'))])))], label='Step With Options'))], blank=True, help_text='A step may have a basic text step or an options accordion which reveals two or more options', verbose_name='Write out the steps a resident needs to take to use the service'),
        ),
        migrations.AlterField(
            model_name='servicepage',
            name='steps_ar',
            field=wagtail.core.fields.StreamField([('basic_step', wagtail.core.blocks.RichTextBlock(features=['ul', 'ol', 'link', 'code', 'rich-text-button-link'], label='Basic Step')), ('step_with_options_accordian', wagtail.core.blocks.StructBlock([('options_description', wagtail.core.blocks.RichTextBlock(classname='odd-placeholder odd-value_Option-description', features=['ul', 'ol', 'link', 'code', 'rich-text-button-link'])), ('options', wagtail.core.blocks.ListBlock(wagtail.core.blocks.StructBlock([('option_name', wagtail.core.blocks.TextBlock(label='Option name. (When clicked, this name will expand the content for this option')), ('option_description', wagtail.core.blocks.RichTextBlock(features=['ul', 'ol', 'link', 'code', 'rich-text-button-link'], label='Option Content'))])))], label='Step With Options'))], blank=True, help_text='A step may have a basic text step or an options accordion which reveals two or more options', null=True, verbose_name='Write out the steps a resident needs to take to use the service'),
        ),
        migrations.AlterField(
            model_name='servicepage',
            name='steps_en',
            field=wagtail.core.fields.StreamField([('basic_step', wagtail.core.blocks.RichTextBlock(features=['ul', 'ol', 'link', 'code', 'rich-text-button-link'], label='Basic Step')), ('step_with_options_accordian', wagtail.core.blocks.StructBlock([('options_description', wagtail.core.blocks.RichTextBlock(classname='odd-placeholder odd-value_Option-description', features=['ul', 'ol', 'link', 'code', 'rich-text-button-link'])), ('options', wagtail.core.blocks.ListBlock(wagtail.core.blocks.StructBlock([('option_name', wagtail.core.blocks.TextBlock(label='Option name. (When clicked, this name will expand the content for this option')), ('option_description', wagtail.core.blocks.RichTextBlock(features=['ul', 'ol', 'link', 'code', 'rich-text-button-link'], label='Option Content'))])))], label='Step With Options'))], blank=True, help_text='A step may have a basic text step or an options accordion which reveals two or more options', null=True, verbose_name='Write out the steps a resident needs to take to use the service'),
        ),
        migrations.AlterField(
            model_name='servicepage',
            name='steps_es',
            field=wagtail.core.fields.StreamField([('basic_step', wagtail.core.blocks.RichTextBlock(features=['ul', 'ol', 'link', 'code', 'rich-text-button-link'], label='Basic Step')), ('step_with_options_accordian', wagtail.core.blocks.StructBlock([('options_description', wagtail.core.blocks.RichTextBlock(classname='odd-placeholder odd-value_Option-description', features=['ul', 'ol', 'link', 'code', 'rich-text-button-link'])), ('options', wagtail.core.blocks.ListBlock(wagtail.core.blocks.StructBlock([('option_name', wagtail.core.blocks.TextBlock(label='Option name. (When clicked, this name will expand the content for this option')), ('option_description', wagtail.core.blocks.RichTextBlock(features=['ul', 'ol', 'link', 'code', 'rich-text-button-link'], label='Option Content'))])))], label='Step With Options'))], blank=True, help_text='A step may have a basic text step or an options accordion which reveals two or more options', null=True, verbose_name='Write out the steps a resident needs to take to use the service'),
        ),
        migrations.AlterField(
            model_name='servicepage',
            name='steps_vi',
            field=wagtail.core.fields.StreamField([('basic_step', wagtail.core.blocks.RichTextBlock(features=['ul', 'ol', 'link', 'code', 'rich-text-button-link'], label='Basic Step')), ('step_with_options_accordian', wagtail.core.blocks.StructBlock([('options_description', wagtail.core.blocks.RichTextBlock(classname='odd-placeholder odd-value_Option-description', features=['ul', 'ol', 'link', 'code', 'rich-text-button-link'])), ('options', wagtail.core.blocks.ListBlock(wagtail.core.blocks.StructBlock([('option_name', wagtail.core.blocks.TextBlock(label='Option name. (When clicked, this name will expand the content for this option')), ('option_description', wagtail.core.blocks.RichTextBlock(features=['ul', 'ol', 'link', 'code', 'rich-text-button-link'], label='Option Content'))])))], label='Step With Options'))], blank=True, help_text='A step may have a basic text step or an options accordion which reveals two or more options', null=True, verbose_name='Write out the steps a resident needs to take to use the service'),
        ),
    ]
