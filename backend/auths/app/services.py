from django.utils import timezone

from rest_framework.response import Response
from rest_framework import status

from .models import (
    User,
    AuthCode,
)

import abc
import random
import pika
import json


class AuthCodeHandlerInterface(metaclass=abc.ABCMeta):
    """
    Interface for AuthCode handlers.
    """
    @classmethod
    @abc.abstractmethod
    def handle(data: dict) -> Response:
        pass


class ActivateAccountHandler(AuthCodeHandlerInterface):
    """
    Handler of activate account codes.
    """
    @classmethod
    @abc.abstractmethod
    def handle(cls, data: dict) -> Response:
        email: str = data.get('email')
        code: str = data.get('code')

        user: User | None = User.objects.filter(email=email).last()

        if not user:
            return Response({'errors': ['Пользователя с таким email не существует.']},  # noqa: E501
                            status.HTTP_400_BAD_REQUEST)

        if user.is_active:
            return Response({'errors': ['Пользователь уже активирован.']},
                            status.HTTP_400_BAD_REQUEST)

        auth_code: AuthCode | None = user.auth_codes.filter(
            code_type=AuthCode.ACTIVATE_ACCOUNT_CODE,
            code=code, expires_at__gt=timezone.now()
        ).last()

        if not auth_code:
            return Response({'errors': ['Данный код не найден.']},
                            status.HTTP_400_BAD_REQUEST)

        user.is_active = True
        user.save(update_fields=('is_active',))

        return Response({'data': ['Аккаунт активирован.']}, status.HTTP_200_OK)


class RestorePasswordHandler(AuthCodeHandlerInterface):
    """
    Handler of restore passwords codes.
    """
    @classmethod
    @abc.abstractmethod
    def handle(cls, data: dict) -> Response:
        email: str = data.get('email')
        code: str = data.get('code')

        user: User | None = User.objects.filter(email=email).last()

        if not user:
            return Response({'errors': ['Пользователя с таким email не существует.']},  # noqa: E501
                            status.HTTP_400_BAD_REQUEST)

        auth_code: AuthCode | None = user.auth_codes.filter(
            code_type=AuthCode.RESET_PASSWORD_CODE,
            code=code, expires_at__gt=timezone.now()
        ).last()

        if not auth_code:
            return Response({'errors': ['Данный код не найден.']},
                            status.HTTP_400_BAD_REQUEST)

        new_password = ''
        for _ in range(3):
            new_password += chr(random.randrange(65, 91))
        for _ in range(5):
            new_password += chr(random.randrange(97, 123))
        for _ in range(3):
            new_password += chr(random.randrange(48, 58))

        message_body = (
            f'Здравствуйте, {user.full_name}!\n'
            f'Вот ваш новый пароль: {new_password}\n'
            'Если вы не требовали восстановление пароля, то просто проигнорируйте это сообщение\n'
            'Если у вас возникли вопросы или проблемы, вы можете связаться с нами по одному из контактов внизу главной страницы сайта.\n'
            'С уважением,\n'
            'Команда Sport WebSite'
        )
        connection = pika.BlockingConnection(
            pika.ConnectionParameters('localhost')
        )
        channel = connection.channel()
        channel.queue_declare(queue='email_queue')
        message: str = json.dumps(
            {
                'send_to': user.email,
                'subject': 'Новый пароль',
                'message': message_body,
            }
        )
        channel.basic_publish(
            exchange='', routing_key='email_queue', body=message
        )

        connection.close()

        user.set_password(new_password)
        user.save()

        return Response({'data': ['На почту выслан новый пароль.']}, status.HTTP_200_OK)
