from django import template
import graphene
import os
from base.models import Topic, Theme

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

STYLEGUIDE_PAGES = {
  'service page': '/writing-service-pages/',
  'process page': '/writing-process-pages/'
}

@register.simple_tag
def get_style_guide_url(*args, **kwargs):
  content_type = kwargs['content_type'].name
  return os.environ['STYLEGUIDE_URL'] + STYLEGUIDE_PAGES[content_type]

@register.inclusion_tag('wagtailadmin/themes.html', takes_context=True)
def themes(context):
    themes = {}
    topics = []

    for theme in Theme.objects.all():
        themes[theme.pk] = {
            'text': theme.text,
            'topics': []
        }

    for topic in Topic.objects.all():
        themes[topic.theme.id]['topics'].append({
            'text': topic.text,
            'id': topic.id,
        })

    return {
        'themes': themes,
        'request': context['request'],
    }
