# Generated by Django 2.2.9 on 2020-01-18 00:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0006_auto_20200118_0042'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='locationpage',
            name='friday_open',
        ),
        migrations.RemoveField(
            model_name='locationpage',
            name='monday_open',
        ),
        migrations.RemoveField(
            model_name='locationpage',
            name='saturday_open',
        ),
        migrations.RemoveField(
            model_name='locationpage',
            name='sunday_open',
        ),
        migrations.RemoveField(
            model_name='locationpage',
            name='thursday_open',
        ),
        migrations.RemoveField(
            model_name='locationpage',
            name='tuesday_open',
        ),
        migrations.RemoveField(
            model_name='locationpage',
            name='wednesday_open',
        ),
        migrations.RemoveField(
            model_name='locationpagerelatedservices',
            name='friday_open',
        ),
        migrations.RemoveField(
            model_name='locationpagerelatedservices',
            name='monday_open',
        ),
        migrations.RemoveField(
            model_name='locationpagerelatedservices',
            name='saturday_open',
        ),
        migrations.RemoveField(
            model_name='locationpagerelatedservices',
            name='sunday_open',
        ),
        migrations.RemoveField(
            model_name='locationpagerelatedservices',
            name='thursday_open',
        ),
        migrations.RemoveField(
            model_name='locationpagerelatedservices',
            name='tuesday_open',
        ),
        migrations.RemoveField(
            model_name='locationpagerelatedservices',
            name='wednesday_open',
        ),
    ]
