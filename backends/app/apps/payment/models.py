from django.db import models
from apps.chats.models import Consultation
from apps.users.models import User


class Accounts(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)


class Transactions(models.Model):
    account_id = models.ForeignKey(Accounts, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, default="in progress")
    date = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    consultation_id = models.ForeignKey(
        Consultation, on_delete=models.CASCADE)
