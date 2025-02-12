# Generated by Django 3.2.4 on 2023-05-23 10:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('comman', '0001_initial'),
        ('panelbuilding', '0001_initial'),
        ('prescreener', '0001_initial'),
        ('panelengagement', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='pecampaigncampaignprescreenerquestionlibrarypage',
            name='campaign',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='panelbuilding.campaign'),
        ),
        migrations.AddField(
            model_name='pecampaigncampaignprescreenerquestionlibrarypage',
            name='page',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='pe_questionlibrary', to='comman.page'),
        ),
        migrations.AddField(
            model_name='pecampaigncampaignprescreenerquestionlibrarypage',
            name='pe_campaign',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='pecampaign', to='panelengagement.pecampaign'),
        ),
        migrations.AddField(
            model_name='pecampaigncampaignprescreenerquestionlibrarypage',
            name='prescreener',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='prescreener.prescreener'),
        ),
        migrations.AddField(
            model_name='pecampaigncampaignprescreenerquestionlibrarypage',
            name='question_library',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='pe_questionlibrary', to='prescreener.questionlibrary'),
        ),
        migrations.AddField(
            model_name='pageroutinglogic',
            name='campaign',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='panelbuilding.campaign'),
        ),
        migrations.AddField(
            model_name='pageroutinglogic',
            name='page',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='comman.page'),
        ),
        migrations.AddField(
            model_name='pageroutinglogic',
            name='pe_campaign',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='panelengagement.pecampaign'),
        ),
        migrations.AddField(
            model_name='pageroutinglogic',
            name='prescreener',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='prescreener.prescreener'),
        ),
        migrations.AddField(
            model_name='pagepipinglogic',
            name='page',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='comman.page'),
        ),
        migrations.AddField(
            model_name='pagemaskinglogic',
            name='page',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='comman.page'),
        ),
        migrations.AddField(
            model_name='page',
            name='campaign',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='panelbuilding.campaign'),
        ),
        migrations.AddField(
            model_name='page',
            name='end_template_page',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='comman.customizethankyouandterminatepage'),
        ),
        migrations.AddField(
            model_name='page',
            name='pe_campaign',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='panelengagement.pecampaign'),
        ),
        migrations.AddField(
            model_name='page',
            name='prescreener',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='prescreener.prescreener'),
        ),
    ]
