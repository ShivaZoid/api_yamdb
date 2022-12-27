from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from .models import User
from .permissions import UserIsAdmin
from .serializers import UserSerializer


class UserViewSet(mixins.CreateModelMixin,
                  mixins.ListModelMixin,
                  GenericViewSet,):
    """
    Создание и просмотр данных пользователя
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (UserIsAdmin,)
    #filter_backends
    #search_fields
    #throttle_classes