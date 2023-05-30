from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.users.models import User


class Bot(models.Model):
    name = models.CharField(_('name'), max_length=256, blank=True)
    img = models.ImageField(_('image'), blank=True, null=True)
    token = models.CharField(_('token'), unique=True, max_length=256)
    lang = models.CharField(_('language'), default='RUS',
                            max_length=5, blank=True)
    desc = models.CharField(_('description'), blank=True, max_length=512)
    start_mes = models.TextField(
        _('start message'), blank=True, max_length=512)
    admin = models.ForeignKey(
        User, on_delete=models.CASCADE)
    date_create = models.DateField(_("date create"), auto_now_add=True)
    date_update = models.DateTimeField(_("date updated"), auto_now=True)

    def __str__(self) -> str:
        return self.name + ' ' + self.token

    class Meta:
        verbose_name = 'bot'
        verbose_name_plural = 'bots'
