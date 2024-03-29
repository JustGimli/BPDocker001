# Generated by Django 4.2.2 on 2023-08-06 18:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='Новый проект', max_length=64)),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='ProjectSettings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('send_type', models.CharField(default='all', max_length=15)),
                ('report_message', models.BooleanField(default=True)),
                ('report_message_type', models.CharField(default='all', max_length=15)),
                ('admin_send_type', models.CharField(default='published', max_length=32)),
                ('timezone', models.CharField(default='Europe/Moscow', max_length=32)),
                ('project', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='projects.project')),
            ],
        ),
    ]
