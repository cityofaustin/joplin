from django import template
from base.models import Topic

register = template.Library()

# Topic snippets
@register.inclusion_tag('wagtailadmin/topics.html', takes_context=True)
def topics(context):
    return {
        'topics': Topic.objects.all(),
        'request': context['request'],
    }
