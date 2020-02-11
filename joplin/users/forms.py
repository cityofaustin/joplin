# from django import forms
# from django.utils.translation import ugettext_lazy as _
#
# from wagtail.users.forms import UserEditForm
# from django.contrib.auth.models import Group
#
# class JoplinUserEditForm(UserEditForm):
#     def get_choices():
#         blarg = Group.objects.all()
#         return [('FR', 'Freshman'), ('SO', 'Sophomore'), ]
#
#     departments = forms.ChoiceField(required=True, label=_("Department"), choices=get_choices())
#
