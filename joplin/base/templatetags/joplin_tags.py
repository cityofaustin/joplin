from django import template
import graphene
import os

register = template.Library()

@register.simple_tag
def get_preview_url(*args, **kwargs):
    revision = kwargs['revision']
    page_type = type(revision.page).__name__

    # TODO: Add other page types
    if "Service" in page_type:
      url_page_type = "service"

    global_id = graphene.Node.to_global_id('PageRevisionNode', revision.id)
    # TODO: Add other languages
    return os.environ["JANIS_URL"] + "/en/preview/" + url_page_type + "/" + global_id
