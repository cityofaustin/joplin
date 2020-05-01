from django import template

register = template.Library()


# Get the groups for a user
@register.filter(name='get_user_groups')
def get_user_groups(form):
    return form['groups'].value() or []


# Get custom validation errors from our "department" and "roles" fields.
@register.filter(name='get_user_errors')
def get_user_errors(form):
    error_messages = {}
    if hasattr(form, "_errors") and form._errors:
        form_errors = form._errors
        if form_errors:
            department_errors = form_errors.get('department')
            if department_errors:
                error_messages["department"] = department_errors.data[0].message
            role_errors = form_errors.get('roles')
            if role_errors:
                error_messages["roles"] = role_errors.data[0].message
    return error_messages
