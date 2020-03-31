from django import template

register = template.Library()

@register.filter(name='get_user_groups')
def get_user_groups(form):
    return form['groups'].value() or []
