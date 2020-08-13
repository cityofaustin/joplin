from django import forms
from django.utils.translation import ugettext_lazy as _
from wagtail.users.forms import UserEditForm, UserCreationForm
from django.core.exceptions import ValidationError

from django.contrib.auth.models import Group
from groups.models import Department, AdditionalGroup


'''
    Overwrite clean() method for Users.
    Ensure that non-admins choose both a Role and a Department.
    Consolidate user-selected "Roles" and "Department" into "Groups".
'''
def custom_user_clean(self, cleaned_data):
    '''
        Why do we have this weird is_superuser fallback?
        Because if a user is editing their own information, they cannot toggle their own superuser status.
        "is_superuser" is determined by the "Administrator" checkbox on the edit user page.
        However, the "Administrator" Checkbox won't show up for you when you're editing your own user.
        A user can neither make themselves an admin nor make themselves not an admin.
        cleaned_data only passes data submitted from the frontend form.
        So cleaned_data will not contain "is_superuser" if you're editing your own user.

        So then how can we tell if you are a superuser or not?
        There is a property called "self.initial" that contains the previous state of user data.
        So if cleaned_data doesn't have "is_superuser", then we can assume that it's because a user is editing themselves.
        And their is_superuser status will be in their prior data.
        Note: we only want to check self.initial if cleaned_data.get("is_superuser") is None and does not exist, not if its False.
    '''
    is_superuser = cleaned_data.get("is_superuser")
    if is_superuser is None:
        is_superuser = self.initial.get("is_superuser")

    group_pks = []
    if cleaned_data["department"]:
        group_pks.append(cleaned_data["department"].pk)
    elif not is_superuser:
        self.add_error("department", ValidationError("Non-Administrators must belong to one Department."))
    if cleaned_data["roles"]:
        for role in cleaned_data["roles"]:
            group_pks.append(role.pk)
    elif not is_superuser:
        self.add_error("roles", ValidationError("Non-Administrators must have at least one Role."))
    if cleaned_data["additional_groups"]:
        for role in cleaned_data["additional_groups"]:
            group_pks.append(role.pk)
    if group_pks:
        cleaned_data["groups"] = Group.objects.filter(pk__in=group_pks)

    return cleaned_data

roles_form = forms.ModelMultipleChoiceField(queryset=Group.objects.filter(name__in=["Moderators", "Editors"]), widget=forms.CheckboxSelectMultiple, required=False, label=_("Roles"))
department_form = forms.ModelChoiceField(queryset=Department.objects, required=False, label=_("Department"))
additional_groups_form = forms.ModelMultipleChoiceField(queryset=AdditionalGroup.objects, widget=forms.CheckboxSelectMultiple, required=False, label=_("Optional Groups"))

# Have to edit both classes, and both templates
# http://docs.wagtail.io/en/v2.1.1/advanced_topics/customisation/custom_user_models.html
class CustomUserEditForm(UserEditForm):
    def clean(self):
        return custom_user_clean(self, super(CustomUserEditForm, self).clean())
    roles = roles_form
    department = department_form
    additional_groups = additional_groups_form


class CustomUserCreationForm(UserCreationForm):
    def clean(self):
        return custom_user_clean(self, super(CustomUserCreationForm, self).clean())
    roles = roles_form
    department = department_form
    additional_groups = additional_groups_form
