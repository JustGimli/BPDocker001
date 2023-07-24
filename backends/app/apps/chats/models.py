from django.db import models
from apps.users.models import User
from apps.botusers.models import BotUsers


class Message(models.Model):
    text = models.CharField(max_length=512, default="", blank=True)
    document = models.FileField(
        upload_to='messages/%Y/', blank=True, null=True)
    photo = models.ImageField(upload_to='messages/%Y/', blank=True, null=True)
    video = models.FileField(upload_to='messages/%Y/', blank=True, null=True)
    is_read = models.BooleanField(default=False)
    time = models.DateTimeField(auto_now_add=True)
    is_author = models.BooleanField(default=False)
    is_bot = models.BooleanField(default=False)

    class Meta:
        indexes = [
            models.Index(fields=['id'])
        ]


class Chat(models.Model):
    chat_id = models.CharField(default=None, unique=True)
    expert = models.ForeignKey(
        User, related_name='users', on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(
        BotUsers, on_delete=models.CASCADE, null=True)
    messages = models.ManyToManyField(Message, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    note = models.TextField(null=True)

    class Meta:
        unique_together = ('chat_id', 'user')

        indexes = [
            models.Index(fields=['id'])
        ]
