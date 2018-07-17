from django import template

register = template.Library()

@register.simple_tag
def global_id(*args, **kwargs):
    revision = kwargs['revision']
    return revision
