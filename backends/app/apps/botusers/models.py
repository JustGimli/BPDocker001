from django.db import models
from apps.bots.models import Bot

class BotUsers(models.Model):
    bot = models.ForeignKey(Bot, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=64, null=True)
    last_name = models.CharField(max_length=64, null=True)
    username = models.CharField(max_length=64)
    registration_date = models.DateTimeField(auto_now_add=True)
    is_have_consultation = models.BooleanField(default=False)
    phone = models.CharField(max_length=15, null=True)
    params = models.JSONField(null=True)
    class Meta:
        unique_together = ('bot', 'username')


class BotUsersStat(models.Model):
    total_messages_recieved = models.PositiveIntegerField(default=0)
    total_messages_sent = models.PositiveIntegerField(default=0)
    last_interation_date = models.DateTimeField(null=True, auto_now=True)