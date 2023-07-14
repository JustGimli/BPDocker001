from django.dispatch import receiver
from djoser.signals import user_activated

from apps.payments.models import Account


@receiver(user_activated)
def user(user, request, **kwargs):
    Account.objects.create(user=user)
