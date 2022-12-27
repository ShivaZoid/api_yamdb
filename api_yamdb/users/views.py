from django.shortcuts import get_object_or_404

from rest_framework.mixins import (
    CreateModelMixin,
    ListModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
)
from rest_framework.viewsets import GenericViewSet
from rest_framework import status
from rest_framework.response import Response

from .models import User
from .permissions import UserIsAdmin, UserIsAuthenticated
from .serializers import UserSerializer
from .exceptions import UserNotFound


class BaseUserSet(CreateModelMixin,
                  ListModelMixin,
                  UpdateModelMixin,
                  DestroyModelMixin,
                  GenericViewSet,):
    """Базовый ViewSet-для реализации CRUD"""
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)

        if request.resolver_match.view_name == 'me':
            instance = User.objects.get(pk=self.request.user.id)
        else:
            instance = get_object_or_404(User, 
                                         username=self.kwargs.get('username'))

        serializer = self.get_serializer(instance, 
                                         data=request.data, 
                                         partial=partial,
                                        )
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}
        return Response(serializer.data)

class AdministrationViewSet(BaseUserSet):
    """
    GET - Получить список всех пользователей. Права доступа: Администратор.
    POST - Добавить нового пользователя. 
           Права доступа: Администратор 
           Поля email и username должны быть уникальными.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (UserIsAdmin,)
    http_method_names = ('get', 'post')
    #filter_backends
    #search_fields
    #throttle_classes


class AdministrationByUsernameViewSet(BaseUserSet,):
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
        user = User.objects.filter(username=self.kwargs.get('username'))
        if not user:
            raise UserNotFound('Такой пользователь отсутствует')
        return user
    
    def destroy(self, request, *args, **kwargs):
        instance = User.objects.filter(username=self.kwargs.get('username'))
        if not instance:
            raise UserNotFound('Такой пользователь отсутствует')
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class AuthUserViewSet(BaseUserSet):
    """
    GET - Получить данные своей учетной записи Права доступа: 
          Любой авторизованный пользователь
    PATCH - Изменить данные своей учетной записи 
            Права доступа: Любой авторизованный пользователь 
            Поля email и username должны быть уникальными.
    """
    serializer_class = UserSerializer
    permission_classes = (UserIsAuthenticated,)
    http_method_names = ('get', 'patch',)

    def get_queryset(self):
        print(self.request.resolver_match.view_name)
        return User.objects.filter(pk=self.request.user.id)
