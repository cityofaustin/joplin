# Generated by Django 2.2.6 on 2019-11-26 17:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0010_auto_20191126_1736'),
    ]

    operations = [
        migrations.AddField(
            model_name='locationpagerelatedservices',
            name='friday_open',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='locationpagerelatedservices',
            name='monday_open',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='locationpagerelatedservices',
            name='saturday_open',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='locationpagerelatedservices',
            name='sunday_open',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='locationpagerelatedservices',
            name='thursday_open',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='locationpagerelatedservices',
            name='tuesday_open',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='locationpagerelatedservices',
            name='wednesday_open',
            field=models.BooleanField(default=False),
        ),
    ]
