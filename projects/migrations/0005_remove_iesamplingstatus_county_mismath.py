# Generated by Django 3.2.4 on 2023-06-19 15:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0004_iesamplingstatus_county_mismath'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='iesamplingstatus',
            name='county_mismath',
        ),
    ]
