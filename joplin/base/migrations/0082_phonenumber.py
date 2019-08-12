# Generated by Django 2.2.4 on 2019-08-12 17:59

from django.db import migrations, models
import django.db.models.deletion
import modelcluster.fields


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0081_auto_20190807_1916'),
    ]

    operations = [
        migrations.CreateModel(
            name='PhoneNumber',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sort_order', models.IntegerField(blank=True, editable=False, null=True)),
                ('phone_description', models.CharField(max_length=255)),
                ('phone_number', models.CharField(max_length=255)),
                ('contact', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='phone_number', to='base.Contact')),
            ],
            options={
                'ordering': ['sort_order'],
                'abstract': False,
            },
        ),
    ]
