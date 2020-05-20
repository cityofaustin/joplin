import os
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

from groups.fixtures.helpers.create_fixture import create_fixture


def editor():
    # they need to at least have the permission to be able to edit pages
    page = ContentType.objects.get(id=15)
    print(page)
    edit_permission = Permission.objects.create(name="can_edit_pages", content_type=page)
    print(edit_permission)
    editor_group = Group.objects.create(name="editor")
    editor_group.permissions.set([edit_permission])
    return editor_group

