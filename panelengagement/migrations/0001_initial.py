# Generated by Django 3.2.4 on 2023-05-23 10:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('account', '0001_initial'),
        ('masters', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PanelistIncentive',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('redemption_id', models.CharField(blank=True, max_length=100, null=True)),
                ('user_survey_id', models.CharField(blank=True, max_length=100, null=True)),
                ('date_of_redemption', models.CharField(blank=True, max_length=100, null=True)),
                ('timestamp_date', models.CharField(blank=True, max_length=100, null=True)),
                ('redemption_value', models.CharField(blank=True, max_length=100, null=True)),
                ('redemption_status', models.CharField(blank=True, max_length=100, null=True)),
                ('ps_catelog_id', models.CharField(blank=True, max_length=100, null=True)),
                ('redeem_choice', models.CharField(blank=True, max_length=100, null=True)),
                ('country', models.CharField(blank=True, max_length=100, null=True)),
                ('source', models.CharField(blank=True, max_length=100, null=True)),
                ('membership_status', models.CharField(blank=True, max_length=100, null=True)),
                ('first_name', models.CharField(blank=True, max_length=100, null=True)),
                ('last_name', models.CharField(blank=True, max_length=100, null=True)),
                ('house_number', models.CharField(blank=True, max_length=100, null=True)),
                ('street', models.CharField(blank=True, max_length=100, null=True)),
                ('city', models.CharField(blank=True, max_length=100, null=True)),
                ('postal_code', models.CharField(blank=True, max_length=100, null=True)),
                ('state', models.CharField(blank=True, max_length=100, null=True)),
                ('mobile_number', models.CharField(blank=True, max_length=100, null=True)),
                ('earned_points', models.CharField(blank=True, max_length=100, null=True)),
                ('spent_points', models.CharField(blank=True, max_length=100, null=True)),
                ('points', models.CharField(blank=True, max_length=100, null=True)),
                ('voucher_code', models.CharField(blank=True, max_length=100, null=True)),
                ('pin', models.CharField(blank=True, max_length=100, null=True)),
                ('amount', models.CharField(blank=True, max_length=100, null=True)),
                ('expiry_date', models.CharField(blank=True, max_length=100, null=True)),
                ('paypal_id', models.CharField(blank=True, max_length=100, null=True)),
                ('paytm_id', models.CharField(blank=True, max_length=100, null=True)),
                ('redemption_source', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Redemption',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('market', models.CharField(blank=True, max_length=100, null=True)),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('threshold_value', models.CharField(blank=True, max_length=100, null=True)),
                ('description', models.CharField(blank=True, max_length=100, null=True)),
                ('image', models.FileField(blank=True, null=True, upload_to='redemption_images/')),
                ('is_instant_redemption', models.BooleanField(default=False)),
                ('is_edenred_redemption', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='PeCampaign',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('campaign_name', models.CharField(blank=True, max_length=100, null=True)),
                ('points', models.CharField(blank=True, max_length=100, null=True)),
                ('status', models.CharField(blank=True, max_length=100, null=True)),
                ('profile_type', models.CharField(blank=True, max_length=100, null=True)),
                ('external_profile_link', models.URLField(blank=True, null=True)),
                ('internal_campaign_generated_link', models.URLField(blank=True, null=True)),
                ('created_date', models.DateField(auto_now_add=True, null=True)),
                ('updated_dateTime', models.DateTimeField(auto_now_add=True, null=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='pe_campaign_created_by', to='account.customuser')),
                ('market', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='masters.country')),
                ('pe_campaign_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='pe_campaign_type', to='masters.pecampaigntype')),
                ('pe_category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='pe_category', to='masters.pecategory')),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='pe_campaign_updated_by', to='account.customuser')),
            ],
        ),
        migrations.CreateModel(
            name='MarketWiseRedemption',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('market', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='masters.country')),
                ('redemption', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='panelengagement.redemption')),
            ],
        ),
    ]
