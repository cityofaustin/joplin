from wagtail.core import blocks
from wagtail.snippets.blocks import SnippetChooserBlock
from django import forms


class MapBlock(blocks.StructBlock):
    marker_description = blocks.RichTextBlock(default="this would be the place name above")
    marker_title = blocks.CharBlock(max_length=120,
                                    default="This would be all the address fields above")
    zoom_level = blocks.IntegerBlock(min_value=0, max_value=18, default='2', required=False)
    location_x = blocks.FloatBlock(default='30.26', required=False)
    location_y = blocks.FloatBlock(default='-97.73', required=False)
    marker_x = blocks.FloatBlock(default='30.26', required=False)
    marker_y = blocks.FloatBlock(default='-97.73', required=False)

    @property
    def media(self):
        return forms.Media(
            js=["https://unpkg.com/leaflet@1.5.1/dist/leaflet.js"],
            css={'all': ["https://unpkg.com/leaflet@1.5.1/dist/leaflet.css"]}
        )

    class Meta:
        form_template = 'wagtailadmin/blocks/map.html'


class SnippetChooserBlockWithAPIGoodness(SnippetChooserBlock):
    def get_api_representation(self, model_instance, context=None):
        return model_instance.serializable_data()


class WhatDoIDoWithBlock(blocks.StaticBlock):
    class Meta:
        icon = 'bin'
        label = 'What do I do with...'
        admin_text = label


class CollectionScheduleBlock(blocks.StaticBlock):
    class Meta:
        icon = 'bin'
        label = 'Collection Schedule'
        admin_text = label


class RecollectBlock(blocks.StaticBlock):
    class Meta:
        icon = 'bin'
        label = 'Recollect'
        admin_text = label
