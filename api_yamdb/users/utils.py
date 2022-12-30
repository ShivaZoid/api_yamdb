from rest_framework_simplejwt.tokens import RefreshToken
from django.core.mail import send_mail


def get_tokens_for_user(user):
    """Получение JWT токенов."""
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


def send_confirm_code(username, email, confirmation_code):
    """Отправление письма с кодом подтверждения."""
    message = (
        f'Для получения токена на портале yamdb неообходимо,\n'
        f'отправить POST запрос на адрес /api/v1/auth/token/\n'
        f'с полями:\nusername - {username}\n'
        f'confirmation_code - {confirmation_code}'
        )
    send_mail(
        subject='Код для подтверждения учетной записи yambd',
        message=message,
        recipient_list=[email,],
        from_email=None,
        fail_silently=False,
    )