from django.db import models
from django.utils.translation import gettext_lazy as _


class Rating(models.Model):
    name = models.CharField(_('name'), max_length=56)
    surname = models.CharField(_('surname'), max_length=56)
    img = models.ImageField(
        _('image'), upload_to='rating/%Y/%m/%d/', blank=True)
    stars = models.DecimalField(_('stars'), decimal_places=0, max_digits=1)
    desc = models.CharField(_('description'), max_length=256, blank=True)
    label = models.CharField(
        _('label name'), max_length=256, default='Врач-педиатр')

    def __str__(self) -> str:
        return self.name + ' ' + self.surname

    class Meta:
        verbose_name = 'rating'
        verbose_name_plural = 'ratings'
