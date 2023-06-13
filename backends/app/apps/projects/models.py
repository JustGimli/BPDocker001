from django.db import models
from apps.bots.models import Bot
from apps.users.models import User


class Project(models.Model):
    name = models.CharField(max_length=64, default="Новый проект")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    bots = models.ForeignKey(
        Bot, on_delete=models.CASCADE, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    send_type = models.CharField(max_length=15, default="all")
    report_message = models.BooleanField(default=True)
    report_message_type = models.CharField(max_length=15, default="all")
    admin_send_type = models.CharField(max_length=32, default='published')
    timezone = models.CharField(max_length=32, default='Europe/Moscow')
