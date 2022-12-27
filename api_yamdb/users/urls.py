from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .views import AdminViewSet, AdminByNameViewSet, AuthUserViewSet


router = DefaultRouter()
#router.register('users', AdminViewSet, basename='users')
#router.register('users/me', AuthUserViewSet, basename='me')
#router.register(
#     r'users/(?P<username>[\w.@+-]+)', 
#     AdminByNameViewSet,
#     basename='username')

users_methods = AdminViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
usernames_methods = AdminByNameViewSet.as_view({
    'get': 'list',
    'patch': 'partial_update',
    'delete': 'destroy',
})
me_methods = AuthUserViewSet.as_view({
    'get': 'list',
    'patch': 'partial_update',
})

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/users/', users_methods, name='users'),
    path('v1/users/me/', me_methods, name='me'),
    path('v1/users/<username>/', usernames_methods, name='usernames'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]