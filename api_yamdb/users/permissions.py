from rest_framework.permissions import IsAdminUser, IsAuthenticated


class UserIsAdmin(IsAdminUser):
    ...


class UserIsAuthenticated(IsAuthenticated):
    ...