from django.shortcuts import get_object_or_404

from rest_framework.filters import SearchFilter
from rest_framework.mixins import (
    CreateModelMixin,
    ListModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
)
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.status import HTTP_204_NO_CONTENT, HTTP_200_OK
from rest_framework.viewsets import GenericViewSet

from .exceptions import UserNotFound
from .models import User
from .permissions import SuperUserOrAdmin, UserIsAuthenticated
from .serializers import (
    UserSerializer,
    SignUpSerializer,
    ReceiveJWTSerializer,
)


class BaseUserSet(CreateModelMixin,
                  ListModelMixin,
                  UpdateModelMixin,
                  DestroyModelMixin,
                  GenericViewSet,):
    """
    Базовый ViewSet-для реализации CRUD
    - Если запрос на v1/users/me/ берем user-a из request
    - Если запрос на v1/users/<username>/ берем usera из kwargs
    """

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)

        if request.resolver_match.view_name == 'me':
            instance = User.objects.get(username=self.request.user)
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

    def retrieve(self, request, *args, **kwargs):
        if request.resolver_match.view_name == 'me':
            queryset = self.queryset.get(username=request.user)
        else:
            queryset = self.queryset.get(username=self.kwargs.get('username'))
        serializer = self.serializer_class(queryset)
        return Response(serializer.data)


class AdministrationViewSet(BaseUserSet):
    """
    GET - Получить список всех пользователей. Права доступа: Администратор.
    POST - Добавить нового пользователя.
           Права доступа: Администратор
           Поля email и username должны быть уникальными.
    """
    queryset = User.objects.order_by('id')
    serializer_class = UserSerializer
    permission_classes = (SuperUserOrAdmin,)
    http_method_names = ('get', 'post')
    pagination_class = PageNumberPagination
    filter_backends = (SearchFilter,)
    search_fields = ('username',)


class AdministrationByUsernameViewSet(BaseUserSet,):
    """
    GET - Получить пользователя по username. Права доступа: Администратор
    PATCH - Изменить данные пользователя по username.
            Права доступа: Администратор.
            Поля email и username должны быть уникальными.
    DELETE - Удалить пользователя по username. Права доступа: Администратор.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (SuperUserOrAdmin,)
    pagination_class = None
    http_method_names = ('get', 'patch', 'delete',)

    def destroy(self, request, *args, **kwargs):
        instance = User.objects.filter(username=self.kwargs.get('username'))
        if not instance:
            raise UserNotFound('Такой пользователь отсутствует')
        self.perform_destroy(instance)
        return Response(status=HTTP_204_NO_CONTENT)


class AuthUserViewSet(BaseUserSet):
    """
    GET - Получить данные своей учетной записи Права доступа:
          Любой авторизованный пользователь
    PATCH - Изменить данные своей учетной записи
            Права доступа: Любой авторизованный пользователь
            Поля email и username должны быть уникальными.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (UserIsAuthenticated,)
    pagination_class = None
    http_method_names = ('get', 'patch',)


class SignUpViewSet(BaseUserSet):
    """
    POST - Получить код подтверждения на переданный email.
           Права доступа: Доступно без токена.
           Использовать имя 'me' в качестве username запрещено.
           Поля email и username должны быть уникальными.
    """
    serializer_class = SignUpSerializer
    http_method_names = ('post',)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=HTTP_200_OK, headers=headers)


class ReceiveJWTViewSet(TokenObtainPairView):
    """
    POST - Получение JWT-токена в обмен на username и confirmation code.
           Права доступа: Доступно без токена.
    """
    serializer_class = ReceiveJWTSerializer
    http_method_names = ('post',)
