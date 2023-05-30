from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .managers import UserManger


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        _('email'), max_length=255, blank=False, unique=True)
    first_name = models.CharField(_('first name'), max_length=56, blank=True)
    last_name = models.CharField(_('last name'), max_length=56, blank=True)
    password = models.CharField(_('password'), max_length=512)
    date_joined = models.DateField(_('date joined'), auto_now_add=True)
    is_staff = models.BooleanField(_('is staff'), default=False)
    is_superuser = models.BooleanField(_('is super user'), default=False)
    is_email_validate = models.BooleanField(_('valid email'), default=False)
    is_active = models.BooleanField(_('active'), default=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManger()

    def __str__(self) -> str:
        return self.email
