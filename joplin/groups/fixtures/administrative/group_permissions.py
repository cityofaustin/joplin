from django.contrib.auth.models import Permission, Group


def add_moderator_permissions():
    moderator_group = Group.objects.get(name="Moderators")
    moderator_group.permissions.add(Permission.objects.get(codename="view_extra_panels"))
    moderator_group.permissions.add(Permission.objects.get(codename="add_contact"))
    moderator_group.permissions.add(Permission.objects.get(codename="change_contact"))
    moderator_group.permissions.add(Permission.objects.get(codename="view_contact"))
    moderator_group.permissions.add(Permission.objects.get(codename="view_snippets"))
    moderator_group.permissions.add(Permission.objects.get(codename="view_user"))
    moderator_group.permissions.add(Permission.objects.get(codename="access_admin"))
    moderator_group.permissions.add(Permission.objects.get(codename="add_document"))
    moderator_group.permissions.add(Permission.objects.get(codename="change_document"))
    moderator_group.permissions.add(Permission.objects.get(codename="delete_document"))
    moderator_group.permissions.add(Permission.objects.get(codename="add_image"))
    moderator_group.permissions.add(Permission.objects.get(codename="change_image"))
    moderator_group.permissions.add(Permission.objects.get(codename="delete_image"))


def add_editor_permissions():
    editor_group = Group.objects.get(name="Editors")
    editor_group.permissions.add(Permission.objects.get(codename="view_user"))
    editor_group.permissions.add(Permission.objects.get(codename="access_admin"))
    editor_group.permissions.add(Permission.objects.get(codename="add_document"))
    editor_group.permissions.add(Permission.objects.get(codename="change_document"))
    editor_group.permissions.add(Permission.objects.get(codename="delete_document"))
    editor_group.permissions.add(Permission.objects.get(codename="add_image"))
    editor_group.permissions.add(Permission.objects.get(codename="change_image"))
    editor_group.permissions.add(Permission.objects.get(codename="delete_image"))
