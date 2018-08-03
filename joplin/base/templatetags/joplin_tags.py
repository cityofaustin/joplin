from django import template
import graphene
import os
from base.models import Topic


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
    return os.environ['STYLEGUIDE_URL'] + "/writing-service-pages/"

  if "process" in content_type:
    return os.environ['STYLEGUIDE_URL'] + "/writing-process-pages/"


# Topic snippets
@register.inclusion_tag('wagtailadmin/topics.html', takes_context=True)
def topics(context):
    return {
        'topics': Topic.objects.all(),
        'request': context['request'],
    }
