from django.urls import path

from .views import (
    AdministrationViewSet, 
    AdministrationByUsernameViewSet,
    AuthUserViewSet,
    SendEmailViewSet,
    ReceiveJWTViewSet,
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
get_tokens = ReceiveJWTViewSet.as_view()

urlpatterns = [
    path('v1/auth/signup/', email_methods, name='email'),
    path('v1/auth/token/', get_tokens, name='token'),
    path('v1/users/', users_methods, name='users'),
    path('v1/users/me/', me_methods, name='me'),
    path('v1/users/<username>/', usernames_methods, name='usernames'),
]
