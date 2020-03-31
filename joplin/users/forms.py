from django import forms
from django.utils.translation import ugettext_lazy as _
from wagtail.users.forms import UserEditForm, UserCreationForm
from django.core.exceptions import ValidationError

from django.contrib.auth.models import Group
from groups.models import Department


'''
    Overwrite clean() method for Users.
    Ensure that non-admins choose both a Role and a Department.
    Set user-selected "Roles" and "Department" into "Groups".
'''
def custom_user_clean(self, cleaned_data):
    # Consolidate "roles" and "department" into "groups"
    group_pks = []
    if cleaned_data["department"]:
        group_pks.append(cleaned_data["department"].pk)
    elif not cleaned_data["is_superuser"]:
        self.add_error("department", ValidationError("Non-Administrators must belong to one Department."))
    if cleaned_data["roles"]:
        for role in cleaned_data["roles"]:
            group_pks.append(role.pk)
    elif not cleaned_data["is_superuser"]:
        self.add_error("roles", ValidationError("Non-Administrators must have at least one Role."))
    if group_pks:
        cleaned_data["groups"] = Group.objects.filter(pk__in=group_pks)

    return cleaned_data

# "Roles" are either "Editor" or "Moderator"
roles_form = forms.ModelMultipleChoiceField(queryset=Group.objects.filter(pk__in=[1, 2]), widget=forms.CheckboxSelectMultiple, required=False, label=_("Roles"))
department_form = forms.ModelChoiceField(queryset=Department.objects, required=False, label=_("Department"))


# Have to edit both classes, and both templates
# http://docs.wagtail.io/en/v2.1.1/advanced_topics/customisation/custom_user_models.html
class CustomUserEditForm(UserEditForm):
    def clean(self):
        return custom_user_clean(self, super(CustomUserEditForm, self).clean())
    roles = roles_form
    department = department_form


class CustomUserCreationForm(UserCreationForm):
    def clean(self):
        return custom_user_clean(self, super(CustomUserCreationForm, self).clean())
    roles = roles_form
    department = department_form
