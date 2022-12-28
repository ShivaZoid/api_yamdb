from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import (
    AdministrationViewSet, 
    AdministrationByUsernameViewSet,
    AuthUserViewSet,
    SendEmailViewSet,
    ReciveTokenJWTViewSet
)


users_methods = AdministrationViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
usernames_methods = AdministrationByUsernameViewSet.as_view({
    'get': 'list',
    'patch': 'partial_update',
    'delete': 'destroy',
})
me_methods = AuthUserViewSet.as_view({
    'get': 'list',
    'patch': 'partial_update',
})
email_methods = SendEmailViewSet.as_view({
    'post': 'create',
})
token_methods = ReciveTokenJWTViewSet.as_view()

urlpatterns = [
    path('v1/auth/signup/', email_methods, name='email'),
    path('v1/auth/token/', token_methods, name='token'),
    path('v1/users/', users_methods, name='users'),
    path('v1/users/me/', me_methods, name='me'),
    path('v1/users/<username>/', usernames_methods, name='usernames'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]