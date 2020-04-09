# Generated by Django 2.2.11 on 2020-03-26 10:45

from django.db import migrations, models
import django.db.models.deletion
import modelcluster.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('location_page', '0001_initial'),
        ('contact', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='contact',
            name='location_page',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='location_page.LocationPage', verbose_name='Select a Location'),
        ),
        migrations.AddField(
            model_name='contactdayandduration',
            name='contact',
            field=modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='hours', to='contact.Contact'),
        ),
    ]