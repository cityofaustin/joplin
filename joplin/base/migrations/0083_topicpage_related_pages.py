# Generated by Django 2.2.4 on 2019-08-21 22:47

from django.db import migrations
import modelcluster.fields


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0082_servicepage_related_topics'),
    ]

    operations = [
        migrations.AddField(
            model_name='topicpage',
            name='related_pages',
            field=modelcluster.fields.ParentalManyToManyField(blank=True, to='base.ServicePage'),
        ),
    ]
