from django.db.models import Avg
from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, viewsets
from rest_framework.filters import SearchFilter

from api.filters import TitleFilter
from reviews.models import Title, Category, Genre
from .permissions import IsAdminOrReadOnly
from .serializers import (TitleGetSerializer,
                          TitlePostSerializer,
                          CategorySerializer,
                          GenreSerializer,
                        )


class TitleViewSet(viewsets.ModelViewSet):
    """
    Получить список всех объектов. Права доступа: Доступно без токена
    """

    queryset = Title.objects.annotate(
        rating=Avg('reviews__score')
    ).all()
    filter_backends = (DjangoFilterBackend,)
    http_method_names = ['get', 'post', 'patch', 'delete']
    filter_class = TitleFilter
    permission_classes = (IsAdminOrReadOnly,)

    def get_serializer_class(self):
        if self.request.method in ('POST', 'PATCH'):
            return TitlePostSerializer
        return TitleGetSerializer


class CategoryViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    """
    Получить список всех категорий. Права доступа: Доступно без токена
    """

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly)
    filter_backends = (SearchFilter, )
    search_fields = ('name', )


class GenreViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    """
    Получить список всех жанров. Права доступа: Доступно без токена
    """

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly)
    filter_backends = (SearchFilter,)
    search_fields = ('name', )
