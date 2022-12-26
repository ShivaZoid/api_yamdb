from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    is_admin = models.BooleanField(
    blank=True,
    null=True,
    )
    is_moderator = models.BooleanField(
    blank=True,
    null=True,
    )
    bio = models.TextField(
    'Биография',
    max_length=350,
    blank=True,
    null=True,
    )


    class Meta:
        verbose_name = ("user")
        verbose_name_plural = ("users")
