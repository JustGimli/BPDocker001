# Generated by Django 4.2.2 on 2023-07-14 08:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('chats', '0001_initial'),
        ('botusers', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='chat',
            name='expert',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='users', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='chat',
            name='messages',
            field=models.ManyToManyField(blank=True, to='chats.message'),
        ),
        migrations.AddField(
            model_name='chat',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='botusers.botusers'),
        ),
        migrations.AddIndex(
            model_name='chat',
            index=models.Index(fields=['id'], name='chats_chat_id_089b52_idx'),
        ),
        migrations.AlterUniqueTogether(
            name='chat',
            unique_together={('chat_id', 'user')},
        ),
    ]
