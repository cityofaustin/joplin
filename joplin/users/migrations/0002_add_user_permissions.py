# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


def add_user_permissions(apps, schema_editor):
    # Get model
    Group = apps.get_model('auth.Group')
    ContentType = apps.get_model('contenttypes', 'ContentType')
    Permission = apps.get_model('auth.Permission')

    # retrieve content types
    user_content_type, created = ContentType.objects.get_or_create(model='user')
    wagtail_admin_content_type, created = ContentType.objects.get_or_create(model='admin')
    document_content_type, created = ContentType.objects.get_or_create(model='document')
    image_content_type, created = ContentType.objects.get_or_create(model='image')
    janis_base_content_type, created = ContentType.objects.get_or_create(model='janisbasepage')
    contact_content_type, created = ContentType.objects.get_or_create(model='contact')
    # retrieve groups
    editor_group = Group.objects.get(name="Editors")
    moderator_group = Group.objects.get(name="Moderators")
    # get or create Permissions: on a new test database, the permissions do not exist, so they must be created.
    # https://stackoverflow.com/questions/31539690/django-migration-fails-with-fake-doesnotexist-permission-matching-query-do
    permission, created = Permission.objects.get_or_create(codename="view_user", content_type=user_content_type)
    editor_group.permissions.add(permission.id)
    moderator_group.permissions.add(permission.id)
    print(permission)
    permission, created = Permission.objects.get_or_create(codename="access_admin", content_type=wagtail_admin_content_type)
    editor_group.permissions.add(permission.id)
    moderator_group.permissions.add(permission.id)
    permission, created = Permission.objects.get_or_create(codename="add_document", content_type=document_content_type)
    editor_group.permissions.add(permission.id)
    moderator_group.permissions.add(permission.id)
    permission, created = Permission.objects.get_or_create(codename="change_document", content_type=document_content_type)
    editor_group.permissions.add(permission.id)
    moderator_group.permissions.add(permission.id)
    permission, created = Permission.objects.get_or_create(codename="delete_document", content_type=document_content_type)
    editor_group.permissions.add(permission.id)
    moderator_group.permissions.add(permission.id)
    permission, created = Permission.objects.get_or_create(codename="add_image", content_type=image_content_type)
    editor_group.permissions.add(permission.id)
    moderator_group.permissions.add(permission.id)
    permission, created = Permission.objects.get_or_create(codename="change_image", content_type=image_content_type)
    editor_group.permissions.add(permission.id)
    moderator_group.permissions.add(permission.id)
    permission, created = Permission.objects.get_or_create(codename="delete_image", content_type=image_content_type)
    editor_group.permissions.add(permission.id)
    moderator_group.permissions.add(permission.id)
    # moderator only permissions
    permission, created = Permission.objects.get_or_create(codename="view_extra_panels", content_type=janis_base_content_type)
    moderator_group.permissions.add(permission.id)
    permission, created = Permission.objects.get_or_create(codename="view_snippets", content_type=janis_base_content_type)
    moderator_group.permissions.add(permission.id)
    permission, created = Permission.objects.get_or_create(codename="add_contact", content_type=contact_content_type)
    moderator_group.permissions.add(permission.id)
    permission, created = Permission.objects.get_or_create(codename="change_contact", content_type=contact_content_type)
    moderator_group.permissions.add(permission.id)
    permission, created = Permission.objects.get_or_create(codename="view_contact", content_type=contact_content_type)
    moderator_group.permissions.add(permission.id)


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(add_user_permissions),
    ]
