from django import template
import os
import json

from snippets.theme.models import Theme
from groups.models import Department
from wagtail.core import hooks
import itertools

register = template.Library()


@register.simple_tag
def get_revision_preview_url(*args, **kwargs):
    revision = kwargs['revision']
    return revision.page.janis_preview_url(revision)


STYLEGUIDE_PAGES = {
    'service page': '/pick-the-perfect-content-type/service-page',
    'process page': '/pick-the-perfect-content-type/process-page',
    'information page': '/pick-the-perfect-content-type/information-page',
    'department page': '/pick-the-perfect-content-type/department-page',
    'location page': '/pick-the-perfect-content-type/location-page',
    'topic page': '',
    'topic collection page': '',
    'official document page': '/pick-the-perfect-content-type/official-documents-page',
    'guide page': '',
    'form container': '',
}


@register.simple_tag
def get_style_guide_url(*args, **kwargs):
    content_type = kwargs['content_type'].name
    try:
        get_style_guide_url = os.getenv('STYLEGUIDE_URL') + STYLEGUIDE_PAGES[content_type]
    except Exception as e:
        get_style_guide_url = os.getenv('STYLEGUIDE_URL')
    return get_style_guide_url


@register.inclusion_tag('wagtailadmin/themes_topics_tree.html', takes_context=True)
def themes_topics_tree(context):
    themes = {}

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

    # If the user is an admin, we need to
    # populate the list of departments for the modal
    if context.request.user.is_superuser:
        for department in Department.objects.all():
            departments.append({
                'title': department.name,
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
    for hook in hooks.get_hooks('construct_page_listing_buttons'):
        hook(buttons, page, page_perms, is_parent, context)

    return {'page': page, 'buttons': buttons}


@register.simple_tag(takes_context=True)
def can_create_topics(context):
    if context.request.user.is_superuser or context.request.user.groups.filter(id=1):
        return True

    return False
