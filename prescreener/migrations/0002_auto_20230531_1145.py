# Generated by Django 3.2.4 on 2023-05-31 06:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prescreener', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='duplicateorfraudpanelistid',
            name='IE',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='duplicateorfraudpanelistid',
            name='browser',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='duplicateorfraudpanelistid',
            name='campaign_id',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='duplicateorfraudpanelistid',
            name='client_id',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='duplicateorfraudpanelistid',
            name='ip_adress',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='duplicateorfraudpanelistid',
            name='os',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='duplicateorfraudpanelistid',
            name='survey_end_time',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='duplicateorfraudpanelistid',
            name='survey_start_time',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='duplicateorfraudpanelistid',
            name='user_country',
            field=models.TextField(blank=True, null=True),
        ),
    ]
