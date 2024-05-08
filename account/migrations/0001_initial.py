# Generated by Django 3.2.4 on 2023-05-23 10:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=150, null=True)),
                ('website', models.CharField(blank=True, max_length=150, null=True)),
                ('create_timestamp', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Create_TimeStamp')),
                ('last_update_timestamp', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Last_update_timestamp')),
            ],
        ),
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(blank=True, max_length=100, null=True)),
                ('first_name', models.CharField(blank=True, max_length=100, null=True)),
                ('last_name', models.CharField(blank=True, max_length=100, null=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('phone_number', models.CharField(blank=True, max_length=150, null=True)),
                ('password', models.CharField(max_length=100)),
                ('isAdmin', models.BooleanField(default=False)),
                ('create_timestamp', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Create_TimeStamp')),
                ('last_update_timestamp', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Last_update_timestamp')),
                ('company', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='company_detail', to='account.company')),
            ],
        ),
        migrations.CreateModel(
            name='UserAccess',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('access', models.JSONField(blank=True, null=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='account.customuser')),
            ],
        ),
        migrations.CreateModel(
            name='RoleAccessControl',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role_name', models.CharField(blank=True, max_length=100, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('create_timestamp', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Create_TimeStamp')),
                ('last_update_timestamp', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Last_update_timestamp')),
                ('company', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='account.company')),
            ],
        ),
        migrations.AddField(
            model_name='customuser',
            name='role',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='role_access', to='account.roleaccesscontrol'),
        ),
    ]
