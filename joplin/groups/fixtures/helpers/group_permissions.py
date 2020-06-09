from django.contrib.auth.models import Permission


def add_moderator_permissions(group):
    group.permissions.add(Permission.objects.get(codename="view_extra_panels").id)
    group.permissions.add(Permission.objects.get(codename="add_contact").id)
    group.permissions.add(Permission.objects.get(codename="change_contact").id)
    group.permissions.add(Permission.objects.get(codename="view_contact").id)
    group.permissions.add(Permission.objects.get(codename="view_snippets").id)
    group.permissions.add(Permission.objects.get(codename="view_user").id)
    group.permissions.add(Permission.objects.get(codename="access_admin").id)
    group.permissions.add(Permission.objects.get(codename="add_document").id)
    group.permissions.add(Permission.objects.get(codename="change_document").id)
    group.permissions.add(Permission.objects.get(codename="delete_document").id)
    group.permissions.add(Permission.objects.get(codename="add_image").id)
    group.permissions.add(Permission.objects.get(codename="change_image").id)
    group.permissions.add(Permission.objects.get(codename="delete_image").id)


def add_editor_permissions(group):
    group.permissions.add(Permission.objects.get(codename="view_user").id)
    group.permissions.add(Permission.objects.get(codename="access_admin").id)
    group.permissions.add(Permission.objects.get(codename="add_document").id)
    group.permissions.add(Permission.objects.get(codename="change_document").id)
    group.permissions.add(Permission.objects.get(codename="delete_document").id)
    group.permissions.add(Permission.objects.get(codename="add_image").id)
    group.permissions.add(Permission.objects.get(codename="change_image").id)
    group.permissions.add(Permission.objects.get(codename="delete_image").id)
