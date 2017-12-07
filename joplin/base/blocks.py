from wagtail.wagtailsnippets.blocks import SnippetChooserBlock


class SnippetChooserBlockWithAPIGoodness(SnippetChooserBlock):
    def get_api_representation(self, model_instance, context=None):
        return model_instance.serializable_data()
