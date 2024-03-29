# Generated by Django 4.2.2 on 2023-08-06 18:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('payments', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='self',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='ip',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='contract',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='account',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddIndex(
            model_name='transaction',
            index=models.Index(fields=['date', 'account'], name='payments_tr_date_07c19a_idx'),
        ),
        migrations.AddIndex(
            model_name='transaction',
            index=models.Index(fields=['account'], name='payments_tr_account_315c16_idx'),
        ),
        migrations.AddIndex(
            model_name='account',
            index=models.Index(fields=['user'], name='payments_ac_user_id_e855b1_idx'),
        ),
    ]
