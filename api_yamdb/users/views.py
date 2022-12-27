from django.shortcuts import get_object_or_404
from django.db.models.query import QuerySet
from rest_framework.mixins import (
            CreateModelMixin,
            ListModelMixin,
            UpdateModelMixin,
            DestroyModelMixin,
        )
from rest_framework.viewsets import GenericViewSet

from .models import User
from .permissions import UserIsAdmin, UserIsAuthenticated
from .serializers import UserSerializer, OneUserSerializer
from .exceptions import UserNotFound

class BaseUserSet(CreateModelMixin,
                  ListModelMixin,
                  UpdateModelMixin,
                  DestroyModelMixin,
                  GenericViewSet,):
    ...

class AdminViewSet(BaseUserSet):
    """
    GET - Получить список всех пользователей. Права доступа: Администратор.
    POST - Добавить нового пользователя. Права доступа: 
           Администратор Поля email и username должны быть уникальными.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (UserIsAdmin,)
    http_method_names = ('get', 'post')
    #filter_backends
    #search_fields
    #throttle_classes


class AdminByNameViewSet(BaseUserSet,):
    """
    GET - Получить пользователя по username. Права доступа: Администратор
    PATCH - Изменить данные пользователя по username. 
           Права доступа: Администратор. 
           Поля email и username должны быть уникальными.
    DELETE - Удалить пользователя по username. Права доступа: Администратор.
    """
    serializer_class = UserSerializer
    permission_classes = (UserIsAdmin,)
    http_method_names = ('get', 'patch', 'delete',)

    def get_queryset(self):
        user = User.objects.filter(username=self.kwargs.get("username"))
        if not user:
            raise UserNotFound('Такой пользователь отсутствует')
        return user


class AuthUserViewSet(BaseUserSet):
    """
    GET - Получить данные своей учетной записи Права доступа: 
          Любой авторизованный пользователь
    PATCH - Изменить данные своей учетной записи Права доступа: 
            Любой авторизованный пользователь 
            Поля email и username должны быть уникальными.
    """
    serializer_class = UserSerializer
    permission_classes = (UserIsAuthenticated,)
    http_method_names = ('get', 'patch',)

    def get_queryset(self):
        return User.objects.filter(pk=self.request.user.id)
