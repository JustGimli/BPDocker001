from django.db import models
from apps.users.models import User
from apps.consultations.models import Scenario
from django.db.models import F


class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10, decimal_places=0, default=0)
    telegram_id = models.CharField(max_length=32, blank=True, null=True)

    class Meta:
        indexes = [
            models.Index(fields=['user'])
        ]

    def get_account(user_id):
        return Account.objects.get(user=user_id)

    def update_balance(user_id, balance):
        Account.objects.select_for_update().\
            filter(pk=user_id)\
            .update(balance=F('balance') + balance)


class Transaction(models.Model):
    account = models.ForeignKey(Account, on_delete=models.PROTECT)
    status = models.CharField(max_length=64, default="in progress")
    date = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(max_digits=10, decimal_places=0)
    consultation = models.ForeignKey(
        Scenario, on_delete=models.SET_NULL, null=True)

    class Meta:
        indexes = [
            models.Index(fields=['date', 'account']),
            models.Index(fields=['account'])
        ]
