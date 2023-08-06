from django.db import models

from apps.users.models import User


class Self(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE)
    series = models.CharField(max_length=32, blank=True)
    number = models.CharField(max_length=32, blank=True)
    issued_place = models.CharField(max_length=64, blank=True)
    issued_date = models.DateField(blank=True)
    division_code = models.CharField(max_length=32, blank=True)
    scan_current = models.FileField(blank=True, null=True)
    scan_self = models.FileField(blank=True, null=True)
    adress = models.CharField(max_length=128, blank=True)
    bank_acc = models.CharField(max_length=32, blank=True)
    bank_name = models.CharField(max_length=128, blank=True)
    bank_inn = models.CharField(max_length=32, blank=True)
    bank_bic = models.CharField(max_length=64, blank=True)
    cor_acc = models.CharField(max_length=128, blank=True)

    @classmethod
    def get_by_user(cls, user):
        return cls.objects.get(user=user)
