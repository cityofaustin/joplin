# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations
from groups.fixtures.helpers import group_permissions


def add_user_permissions(apps, schema_editor):
    # Get model
    Group = apps.get_model('auth.Group')
    Permission = apps.get_model

    editor_group = Group.objects.get(name="Editors")
    group_permissions.add_editor_permissions(editor_group)
    moderator_group = Group.objects.get(name="Moderators")
    group_permissions.add_moderator_permissions(moderator_group)


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(add_user_permissions),
    ]
