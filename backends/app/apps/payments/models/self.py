from django.db import models

from apps.users.models import User


class Passport(models.Model):
    series = models.CharField(max_length=32)
    number = models.CharField(max_length=32)
    issued_place = models.CharField(max_length=64)
    issued_date = models.DateField()
    division_code = models.CharField(max_length=32)


class Self(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE)
    passport = models.ForeignKey(
        Passport, on_delete=models.CASCADE)
    adress = models.CharField(max_length=128)
    bank_acc = models.CharField(max_length=32)
    bank_name = models.CharField(max_length=128)
    bank_inn = models.CharField(max_length=32)
    bank_bic = models.CharField(max_length=64)
    cor_acc = models.CharField(max_length=128)

    @classmethod
    def get_by_user(cls, user):
        return cls.objects.get(user=user)
