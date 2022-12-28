from secrets import token_urlsafe
from django.core.mail import send_mail

from rest_framework.serializers import ModelSerializer, Serializer, CharField

from .models import User, UserRegistration
from .exceptions import UserNotFound, WrongData
from .utils import get_tokens_for_user


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
            #hash
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


class ReceiveJWTSerializer(Serializer):
    
    username = CharField(max_length=60)
    confirmation_code = CharField(max_length=32)
            
    def validate(self, data):
        username = data['username']
        confirmation_code = data['confirmation_code']

        try:
            user_obj = UserRegistration.objects.get(
                            username=username,
                            confirmation_code=confirmation_code)

            tokens = get_tokens_for_user(user_obj)
            user_obj.delete()
            return {'tokens': tokens}
        except Exception:
            raise WrongData('Введены не правильные данные')
