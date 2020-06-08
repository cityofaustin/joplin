from django.contrib.auth.models import Permission


def add_moderator_permissions(group):
    perms_to_add = []
    perms_to_add.append(Permission.objects.get(codename="view_extra_panels"))
    perms_to_add.append(Permission.objects.get(codename="add_contact"))
    perms_to_add.append(Permission.objects.get(codename="change_contact"))
    perms_to_add.append(Permission.objects.get(codename="view_contact"))
    perms_to_add.append(Permission.objects.get(codename="view_snippets"))
    perms_to_add.append(Permission.objects.get(codename="view_user"))
    perms_to_add.append(Permission.objects.get(codename="access_admin"))
    perms_to_add.append(Permission.objects.get(codename="add_document"))
    perms_to_add.append(Permission.objects.get(codename="change_document"))
    perms_to_add.append(Permission.objects.get(codename="delete_document"))
    perms_to_add.append(Permission.objects.get(codename="add_image"))
    perms_to_add.append(Permission.objects.get(codename="change_image"))
    perms_to_add.append(Permission.objects.get(codename="delete_image"))

    group.permissions.add(perms_to_add)


def add_editor_permissions(group):
    perms_to_add = []
    perms_to_add.append(Permission.objects.get(codename="view_user"))
    perms_to_add.append(Permission.objects.get(codename="access_admin"))
    perms_to_add.append(Permission.objects.get(codename="add_document"))
    perms_to_add.append(Permission.objects.get(codename="change_document"))
    perms_to_add.append(Permission.objects.get(codename="delete_document"))
    perms_to_add.append(Permission.objects.get(codename="add_image"))
    perms_to_add.append(Permission.objects.get(codename="change_image"))
    perms_to_add.append(Permission.objects.get(codename="delete_image"))

    group.permissions.add(perms_to_add)
