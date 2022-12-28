from django.core.mail import send_mail
from secrets import token_urlsafe

from rest_framework.serializers import ModelSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import User, UserRegistration
from .exceptions import UserNotFound


class UserSerializer(ModelSerializer):
    class Meta:
        fields = ('username', 'email', 'first_name', 'last_name', 'bio', 
                  'role')
        model = User


class SendEmailSerializer(ModelSerializer):
    class Meta:
        fields = ('username', 'email',)
        model = UserRegistration

    def validate(self, data):
        email = data['email']
        username = data['username']

        if User.objects.filter(email=email, username=username).exists():
            confirmation_code = token_urlsafe(16)
            message = (
                f'Для получения токена на портале yamdb неообходимо,\n'
                f'отправить POST запрос на адрес /api/v1/auth/token/\n'
                f'с полями:\nusername - {username}\n'
                f'confirmation_code - {confirmation_code}'
                )

            data['confirmation_code'] = confirmation_code

            send_mail(
                subject='Код для подтверждения учетной записи yambd',
                message=message,
                recipient_list=['am.alexeev@mail.ru'],
                from_email=None,
                fail_silently=False,
            )
            return data
        else:
            raise UserNotFound(
                'Пользователь с таким username или email отсутствует')


class ReciveTokenSerializer(TokenObtainPairSerializer):
    
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['name'] = user.name
        # ...

        return token
    