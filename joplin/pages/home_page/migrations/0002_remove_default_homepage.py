# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


def remove_default_homepage(apps, schema_editor):
    # Get model
    Page = apps.get_model('wagtailcore.Page')

    # Delete the default homepage
    # If migration is run multiple times, it may have already been deleted
    Page.objects.filter(id=2).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('home_page', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(remove_default_homepage),
    ]
