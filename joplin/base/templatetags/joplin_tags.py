from django import template
import graphene

register = template.Library()

@register.simple_tag
def global_id(*args, **kwargs):
    revision = kwargs['revision']
    revision_id = revision.id
    global_id = graphene.Node.to_global_id('PageRevisionNode', revision_id)
    return global_id
