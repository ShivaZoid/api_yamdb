from re import match
from secrets import token_urlsafe

from django.db.utils import IntegrityError
from django.shortcuts import get_object_or_404
from rest_framework.serializers import (
    ModelSerializer, 
    Serializer, 
    CharField, 
    EmailField
)
from .models import User
from .utils import get_tokens_for_user, send_confirm_code
from .exceptions import (
    UserFound, 
    WrongData, 
    CantChangeRole, 
    NotValidUserName,
)

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'bio', 
                  'role')

    def validate_role(self, value):
        """
        - Только admin и superuser могут изменять поле role.
        """
        if (self.context['request'].user.role != 'admin' and not 
              self.context['request'].user.is_superuser):
            raise CantChangeRole('У вас нету прав для изменения role')
        return value

    def validate(self, data):
        """
        - Если в запросе есть username, проверяем его.
        """
        confirmation_code = token_urlsafe(16)
        data['confirmation_code'] = confirmation_code
        if data.get('username') is not None:
            if match(r'^[\w.@+-]+', data['username']) is None:
                raise NotValidUserName('Не корректный username')
        return data


class SignUpSerializer(Serializer):

    username = CharField(max_length=150)
    email = EmailField(max_length=254)

    def validate(self, data):
        email = data['email']
        username = data['username']

        if not User.objects.filter(email=email, username=username).exists():
            confirmation_code = token_urlsafe(16)
            data['confirmation_code'] = confirmation_code
        if username == 'me':
            raise NotValidUserName('Username "me" запрещен')
        if match(r'^[\w.@+-]+', data['username']) is None:
            raise NotValidUserName('Не корректный username')

        return data

    def create(self, validated_data):
        """
        - Если пользователя зарегестрировал admin отправляем письмо на почту
          и получаем данные из запроса (первый блок try)
        - Если пользователь регистрируется самосстоятельно
          создаем пользователя в бд и отправляем письмо (второй блок try)
        """
        email = validated_data['email']
        username = validated_data['username']
        confirmation_code = validated_data.get('confirmation_code')
        
        try:
            user_obj = User.objects.get(**validated_data)
            confirmation_code = user_obj.confirmation_code
            send_confirm_code(username, email, confirmation_code)
            return validated_data
        
        except Exception:
            try:
                new_user = User.objects.create(**validated_data)
                send_confirm_code(username, email, confirmation_code)
                return new_user
            except IntegrityError:
                raise UserFound(
                    'Пользователь с таким username или email существует') 
            

class ReceiveJWTSerializer(Serializer):
    
    username = CharField(max_length=150)
    confirmation_code = CharField(max_length=32)
            
    def validate(self, data):
        """
        - Если пользователь есть в бд, выдаем токены
        - Иначе 404 ошибка
        """
        username = data['username']
        confirmation_code = data['confirmation_code']
        user = get_object_or_404(User, username=username)
        try:
            user = User.objects.get(username=username,
                                    confirmation_code=confirmation_code)
            tokens = get_tokens_for_user(user)
            # После активации обновлять conf_code в bd
            return {'tokens': tokens}
        except Exception:
            raise WrongData('Введены не правильные данные')
