from django.db import models

from apps.users.models import User


class IP(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    inn = models.CharField(max_length=32)
    ogrn = models.CharField(max_length=32)
    bank_acc = models.CharField(max_length=32)
    bank_name = models.CharField(max_length=128)
    bank_inn = models.CharField(max_length=32)
    bank_bic = models.CharField(max_length=64)
    cor_acc = models.CharField(max_length=128)

    @classmethod
    def get_by_user(cls, user):
        return cls.objects.get(user=user)
