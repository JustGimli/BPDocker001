from django.db import models

from apps.users.models import User
from apps.bots.models import Bot


class Message(models.Model):
    message = models.CharField(max_length=512)
    is_read = models.BooleanField(default=False)
    time = models.DateTimeField(auto_now_add=True)
    is_author = models.BooleanField(default=True)


class Chat(models.Model):
    chat_id = models.IntegerField(default=None)
    user = models.OneToOneField(
        User, related_name='users', on_delete=models.DO_NOTHING, null=True)
    bot = models.OneToOneField(
        Bot, related_name='bot', on_delete=models.DO_NOTHING, null=True)

    sender_id = models.IntegerField(default=None)
    messages = models.ManyToManyField(Message, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('chat_id', 'user', 'bot')


class BotUsers(models.Model):
    bot = models.ForeignKey(Bot, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=64, null=True)
    last_name = models.CharField(max_length=64, null=True)
    username = models.CharField(max_length=64)
    registration_date = models.DateTimeField(auto_now_add=True)
    last_interation_date = models.DateTimeField(null=True, auto_now=True)
    total_messages_recieved = models.PositiveIntegerField(default=0)
    total_messages_sent = models.PositiveIntegerField(default=0)
    is_have_consultation = models.BooleanField(default=False)
    phone = models.CharField(max_length=15, null=True)

    class Meta:
        unique_together = ('bot', 'username')


class Consultation(models.Model):
    user = models.ForeignKey(BotUsers, on_delete=models.CASCADE)
    expert = models.ForeignKey(User, on_delete=models.CASCADE)
    consultation_type = models.CharField(
        max_length=10)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(auto_now=True)
    message_count = models.PositiveIntegerField(default=0)
