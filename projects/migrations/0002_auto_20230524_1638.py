# Generated by Django 3.2.4 on 2023-05-24 11:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='iesamplingstatus',
            name='duplicate_score',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='iesamplingstatus',
            name='threat_potential_score',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
