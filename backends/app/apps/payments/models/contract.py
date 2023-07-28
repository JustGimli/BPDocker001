from django.db import models

from apps.users.models import User


class Contract(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    agreement_flag = models.BooleanField(default=True)
