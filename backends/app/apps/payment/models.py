from django.db import models
from apps.consultations.models import Scenario
from apps.users.models import User


class Account(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, unique=True)
    balance = models.DecimalField(max_digits=10, decimal_places=0, default=0)


class Transaction(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    status = models.CharField(max_length=64, default="in progress")
    date = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(max_digits=10, decimal_places=0)
    consultation = models.ForeignKey(
        Scenario, on_delete=models.CASCADE, null=True)
