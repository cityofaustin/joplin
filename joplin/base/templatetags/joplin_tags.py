from django import template
import graphene
import os
import json

from base.models import Topic, Theme
from wagtail.core import hooks
import itertools

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
def get_live_url(*args, **kwargs):
    page = kwargs['page']
    page_type = type(page).__name__
    page_slug = page.slug

    # TODO: Add other page types
    if "Service" in page_type:
      url_page_type = "services"

    if "Process" in page_type:
      url_page_type = "processes"

    # TODO: Add other languages
    return os.environ["JANIS_URL"] + "/en/" + url_page_type + "/" + page_slug

STYLEGUIDE_PAGES = {
  'service page': '/writing-service-pages/',
  'process page': '/writing-process-pages/'
}

@register.simple_tag
def get_style_guide_url(*args, **kwargs):
  content_type = kwargs['content_type'].name
  return os.environ['STYLEGUIDE_URL'] + STYLEGUIDE_PAGES[content_type]

@register.inclusion_tag('wagtailadmin/themes_topics_tree.html', takes_context=True)
def themes_topics_tree(context):
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
        'themes': json.dumps(themes)
    }


@register.inclusion_tag("wagtailadmin/pages/listing/_buttons.html",
                        takes_context=True)
def joplin_page_listing_buttons(context, page, page_perms, is_parent=False):
    button_hooks = hooks.get_hooks('register_joplin_page_listing_buttons')
    buttons = sorted(itertools.chain.from_iterable(
        hook(page, page_perms, is_parent)
        for hook in button_hooks))
    return {'page': page, 'buttons': buttons}
