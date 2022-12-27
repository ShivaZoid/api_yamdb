from django.db import models
from django.contrib.auth.models import AbstractUser


USER = 'user'
ADMIN = 'admin'
MODERATOR = 'moderator'

ROLE_PERMISSION = [
    (USER, 'Аутентифицированный пользователь'),
    (MODERATOR, 'Модератор'),
    (ADMIN, 'Администратор')
]


class User(AbstractUser):
    """Модель для пользователей.

    Attributes:
        username: отображаемое имя пользователя.
        email: почта пользователя.
        first_name: имя.
        last_name: фамилия.
        bio: биография.
        role: роль(права доступа).
    """

    username = models.CharField(
        max_length=150,
        unique=True,
        blank=False,
        null=False
    )
    email = models.EmailField(
        max_length=254,
        unique=True,
        blank=False,
        null=False
    )
    first_name = models.CharField(
        'Имя',
        max_length=150,
        blank=True
    )
    last_name = models.CharField(
        'Фамилия',
        max_length=150,
        blank=True
    )
    bio = models.TextField(
        'Биография',
        blank=True,
    )
    role = models.CharField(
        'Роль',
        max_length=20,
        choices=ROLE_PERMISSION,
        default=USER,
        blank=True
    )

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = ('User')
        verbose_name_plural = ('Users')