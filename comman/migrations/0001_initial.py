# Generated by Django 3.2.4 on 2023-05-23 10:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('prescreener', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomizeThankyouandTerminatePage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('inline_html_code', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='DashboardData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_clicks', models.IntegerField(blank=True, default=1, null=True)),
                ('total_invite_sent', models.IntegerField(blank=True, default=1, null=True)),
                ('total_completes', models.IntegerField(blank=True, default=1, null=True)),
                ('response_rate', models.FloatField(blank=True, default=1, null=True)),
                ('completion_rate', models.IntegerField(blank=True, default=1, null=True)),
                ('snc', models.IntegerField(blank=True, default=1, null=True)),
                ('completed', models.IntegerField(blank=True, default=1, null=True)),
                ('quotas_full', models.IntegerField(blank=True, default=1, null=True)),
                ('terminated', models.IntegerField(blank=True, default=1, null=True)),
                ('quality_fail', models.IntegerField(blank=True, default=1, null=True)),
                ('panel_duplicate', models.IntegerField(blank=True, default=1, null=True)),
                ('total_soi', models.IntegerField(blank=True, default=1, null=True)),
                ('total_doi', models.IntegerField(blank=True, default=1, null=True)),
                ('total_conversion_rate', models.FloatField(blank=True, default=1, null=True)),
                ('total_spent', models.FloatField(blank=True, default=1, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='EnableRd',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('enable_rd', models.BooleanField(blank=True, default=False, null=True)),
                ('risk', models.JSONField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='PageMaskingLogic',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('question_id', models.IntegerField(blank=True, null=True)),
                ('questio_choice_id', models.IntegerField(blank=True, null=True)),
                ('target_question_id', models.IntegerField(blank=True, null=True)),
                ('hide_answer_id', models.IntegerField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='PagePipingLogic',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('question_id', models.IntegerField(blank=True, null=True)),
                ('next_question_id', models.IntegerField(blank=True, null=True)),
                ('next_question_text', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='PageRoutingLogic',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('logic', models.JSONField(blank=True, null=True)),
                ('targeted_page', models.CharField(blank=True, max_length=100, null=True)),
                ('targeted_page_name', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='PeCampaignCampaignPrescreenerQuestionLibraryPage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='QuestionsLinkedPage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('page', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='comman.page')),
                ('question_library', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='prescreener.questionlibrary')),
            ],
        ),
    ]
