from django.db import models
from django.utils.translation import gettext_lazy as _
from datetime import timedelta
from apps.chats.models import BotUsers
from apps.users.models import User
from apps.bots.models import Bot


class File(models.Model):
    file = models.FileField(upload_to="files/%Y/")


class Scenario(models.Model):
    name = models.CharField(max_length=64, default='Консультация')
    price = models.DecimalField(max_digits=10, decimal_places=0, default=500)
    bot = models.ForeignKey(Bot, on_delete=models.CASCADE)
    start_message = models.CharField(max_length=512, default="Консультация")
    duration = models.DurationField(default=timedelta(days=5))
    date_update = models.DateTimeField(_("date updated"), auto_now=True)
    is_active = models.BooleanField(_("active"), default=True)
    files = models.ManyToManyField(
        File, related_name="scenariosFiles", blank=True)


class Consultation(models.Model):
    user = models.ForeignKey(BotUsers, on_delete=models.CASCADE)
    expert = models.ForeignKey(User, on_delete=models.CASCADE)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(auto_now=True)
    scenario = models.ForeignKey(Scenario, on_delete=models.CASCADE)
    # message_count = models.PositiveIntegerField(default=0)  # primary = models.BooleanField(default=True)
