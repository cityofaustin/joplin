from django import template
import graphene
import os

register = template.Library()

@register.simple_tag
def get_preview_url(*args, **kwargs):
    revision = kwargs['revision']
    # TODO: Add other page types
    if "Service" in kwargs['page_type']:
      page_type = "service"
    print(page_type)
    revision_id = revision.id
    global_id = graphene.Node.to_global_id('PageRevisionNode', revision_id)
    # TODO: Add other languages
    return os.environ["JANIS_URL"] + "/en/preview/" + page_type + "/" + global_id
