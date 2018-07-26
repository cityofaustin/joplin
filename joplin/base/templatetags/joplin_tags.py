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
      url_page_type = "services"

    if "Process" in page_type:
      url_page_type = "processes"

    global_id = graphene.Node.to_global_id('PageRevisionNode', revision.id)
    # TODO: Add other languages
    return os.environ["JANIS_URL"] + "/en/preview/" + url_page_type + "/" + global_id

@register.simple_tag
def get_style_guide_url(*args, **kwargs):
  content_type = kwargs['content_type'].name

  if "service" in content_type:
    return "https://briaguya.github.io/digital-services-style-guide/writing-service-pages/"

  if "process" in content_type:
    return "https://briaguya.github.io/digital-services-style-guide/writing-process-pages/"
