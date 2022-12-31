from rest_framework.exceptions import ValidationError, PermissionDenied


class CantChangeRole(PermissionDenied):
    ...


class UserNotFound(ValidationError):
    ...


class UserFound(ValidationError):
    ...


class WrongData(ValidationError):
    ...


class NotValidUserName(ValidationError):
    ...