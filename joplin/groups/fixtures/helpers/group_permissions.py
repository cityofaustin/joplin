from django.contrib.auth.models import Permission


def add_moderator_permissions(group):
    group.permissions.add(Permission.objects.get(codename="view_extra_panels"))
    group.permissions.add(Permission.objects.get(codename="add_contact"))
    group.permissions.add(Permission.objects.get(codename="change_contact"))
    group.permissions.add(Permission.objects.get(codename="view_contact"))
    group.permissions.add(Permission.objects.get(codename="view_snippets"))
    group.permissions.add(Permission.objects.get(codename="view_user"))
    group.permissions.add(Permission.objects.get(codename="access_admin"))
    group.permissions.add(Permission.objects.get(codename="add_document"))
    group.permissions.add(Permission.objects.get(codename="change_document"))
    group.permissions.add(Permission.objects.get(codename="delete_document"))
    group.permissions.add(Permission.objects.get(codename="add_image"))
    group.permissions.add(Permission.objects.get(codename="change_image"))
    group.permissions.add(Permission.objects.get(codename="delete_image"))


def add_editor_permissions(group):
    group.permissions.add(Permission.objects.get(codename="view_user"))
    group.permissions.add(Permission.objects.get(codename="access_admin"))
    group.permissions.add(Permission.objects.get(codename="add_document"))
    group.permissions.add(Permission.objects.get(codename="change_document"))
    group.permissions.add(Permission.objects.get(codename="delete_document"))
    group.permissions.add(Permission.objects.get(codename="add_image"))
    group.permissions.add(Permission.objects.get(codename="change_image"))
    group.permissions.add(Permission.objects.get(codename="delete_image"))
