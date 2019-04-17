from django import template
import graphene
import os
import json

from base.models import TopicPage, Theme, DepartmentPage
from wagtail.core import hooks
import itertools

register = template.Library()

@register.simple_tag
def get_revision_preview_url(*args, **kwargs):
    revision = kwargs['revision']
    url_page_type = revision.page.janis_url_page_type

    global_id = graphene.Node.to_global_id('PageRevisionNode', revision.id)
    # TODO: Add other languages
    return os.environ["JANIS_URL"] + "/en/preview/" + url_page_type + "/" + global_id

STYLEGUIDE_PAGES = {
  'service page': '/writing-service-pages/',
  'process page': '/writing-process-pages/',
  'information page': '/writing-process-pages/',
  'department page': '/writing-process-pages/',
  'topic page': '/writing-process-pages/',
  'topic collection page': '/writing-process-pages/',
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
            'id': theme.id,
            'topics': []
        }

    return {
        'themes': json.dumps(themes)
    }

@register.inclusion_tag('wagtailadmin/departments_list.html', takes_context=True)
def departments_list(context):
    departments = []

    for department in DepartmentPage.objects.all():
        departments.append({
            'title': department.title,
            'id': department.id,
        })

    return {
        'departments': json.dumps(departments)
    }

@register.inclusion_tag("wagtailadmin/pages/listing/_buttons.html",
                        takes_context=True)
def joplin_page_listing_buttons(context, page, page_perms, is_parent=False):
    button_hooks = hooks.get_hooks('register_joplin_page_listing_buttons')
    buttons = sorted(itertools.chain.from_iterable(
        hook(page, page_perms, is_parent)
        for hook in button_hooks))
    return {'page': page, 'buttons': buttons}
