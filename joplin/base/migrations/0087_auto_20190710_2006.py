# Generated by Django 2.2.3 on 2019-07-10 20:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0086_auto_20190710_1944'),
    ]

    operations = [
        migrations.RenameField(
            model_name='servicepagerelateddepartments',
            old_name='related_departments',
            new_name='related_department',
        ),
    ]
