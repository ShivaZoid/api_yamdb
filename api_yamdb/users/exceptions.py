from rest_framework.serializers import ValidationError


class UserNotFound(ValidationError):
    ...


class WrongData(ValidationError):
    ...
