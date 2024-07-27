from django.shortcuts import (
	render,
	redirect,
)
from django import views
from django.http import (
	HttpRequest,
	HttpResponse,
)
from django.contrib.auth import (
	authenticate,
	login,
)
from django.contrib.auth.mixins import LoginRequiredMixin

from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

import pika
import json


from .serializers import (
	RegistrationSerializer,
	RestorePasswordSerializer,
	AuthCodeSerializer,
)
from .validators import (
	validate_email,
	validate_gender,
	validate_name,
	validate_password,
	validate_age,
	validate_height,
	validate_weight,
	validate_code,
)
from .models import (
	User,
	AuthCode,
)
from .services import (
	ActivateAccountHandler,
	RestorePasswordHandler,
)


class RegistrationView(APIView):
	"""
	View for registration of users.
	"""

	def post(self, request: Request) -> Response:
		serializer: RegistrationSerializer = RegistrationSerializer(
			data=request.data
		)

		if serializer.is_valid():
			data = serializer.validated_data

			context_errors = {}

			is_error, errors = validate_name(data.get('first_name'))
			if is_error:
				context_errors['first_name'] = errors

			is_error, errors = validate_name(data.get('last_name'))
			if is_error:
				context_errors['last_name'] = errors

			is_error, errors = validate_email(data.get('email'))
			if is_error:
				context_errors['email'] = errors

			is_error, errors = validate_password(data.get('password'))
			if is_error:
				context_errors['password'] = errors

			is_error, errors = validate_height(data.get('height'))
			if is_error:
				context_errors['height'] = errors

			is_error, errors = validate_weight(data.get('weight'))
			if is_error:
				context_errors['weight'] = errors

			is_error, errors = validate_age(data.get('birthday'))
			if is_error:
				context_errors['birthday'] = errors

			is_error, errors = validate_gender(data.get('gender'))
			if is_error:
				context_errors['gender'] = errors

			if context_errors:
				return Response(
					{'errors': context_errors}, status.HTTP_401_UNAUTHORIZED
				)

			user: User | None = User.objects.filter(
				email=data.get('email')
			).last()

			if user and user.is_active:
				return Response(
					{'errors': ['Пользователь с таким email уже существует']},
					status.HTTP_401_UNAUTHORIZED,
				)

			user = serializer.save()

			activation_code = AuthCode(user=user)
			activation_code.code_type = AuthCode.ACTIVATE_ACCOUNT_CODE
			activation_code.save()

			message_body = (
				f'Здравствуйте, {user.full_name}!\n'
				'Поздравляем с созданием аккаунта на Sport WebSite.\n'
				'Для завершения регистрации и активации вашего аккаунта, пожалуйста, используйте следующий код активации:\n'  # noqa: E501
				f'Код активации: {activation_code.code}\n'
				f'Срок действия кода: {activation_code.LIFETIME} минут.\n'
				f'Ссылка для ввода кода: http://127.0.0.1:5000/activate-code/{user.email}/2/\n'  # noqa: E501
				'Пожалуйста, введите этот код на странице активации аккаунта.\n'  # noqa: E501
				'Если вы не регистрировались на нашем сайте, проигнорируйте это сообщение. Ваш email не будет использован для активации.\n'  # noqa: E501
				'Если у вас возникли вопросы или проблемы, вы можете связаться с нами по одному из контактов внизу главной страницы сайта.\n'  # noqa: E501
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
					'subject': 'Активация аккаунта',
					'message': message_body,
				}
			)
			channel.basic_publish(
				exchange='', routing_key='email_queue', body=message
			)

			connection.close()

			return Response({}, status.HTTP_201_CREATED)

		err: str | None = serializer.errors.get('email')
		if err and str(err[0]) == 'пользователь с таким почта уже существует.':
			email = request.data.get('email')
			user: User = User.objects.get(email=email)
			if not user.is_active:
				user.delete()
				serializer.is_valid = True
				serializer.save()
				return Response({}, status.HTTP_201_CREATED)
		return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


class LoginView(views.View):
	"""
	View for login of user.
	"""

	def get(self, request: HttpRequest) -> HttpResponse:
		return render(request=request, template_name='auths/login.html')

	def post(self, request: HttpRequest) -> HttpResponse:
		authentication_errors = {'errors': {}}

		email: str = request.POST.get('email')
		password: str = request.POST.get('password')

		is_error, errors = validate_email(email)

		if is_error:
			authentication_errors['errors']['email'] = errors

		is_error, errors = validate_password(password)

		if is_error:
			authentication_errors['errors']['password'] = errors

		if authentication_errors.get('errors'):
			return render(
				request=request,
				template_name='auths/login.html',
				context=authentication_errors,
				status=400,
			)

		user: User | None = authenticate(
			request=request, email=email, password=password
		)

		if not user:
			return render(
				request=request,
				template_name='auths/login.html',
				context={
					'user_not_found': 'Пользователь с таким '
					'логином или паролем не найден'
				},
				status=400,
			)

		login(request=request, user=user)

		return redirect('profile/')


class RestorePasswordView(APIView):
	"""
	View for users to restore their passwords.
	"""

	def post(self, request: Request) -> Response:
		serializer: RestorePasswordSerializer = RestorePasswordSerializer(
			data=request.data
		)

		if serializer.is_valid():
			data = serializer.validated_data

			context_errors = {}

			is_error, errors = validate_email(data.get('email'))
			if is_error:
				context_errors['email'] = errors

			if context_errors:
				return Response(
					{'errors': context_errors}, status.HTTP_400_BAD_REQUEST
				)

			user: User | None = User.objects.filter(
				email=data.get('email')
			).last()

			if not user:
				errors = ['Пользователь с данным email не найден.']
				return Response(
					{'errors': errors}, status.HTTP_400_BAD_REQUEST
				)

			reset_password_code = AuthCode(user=user)
			reset_password_code.code_type = AuthCode.RESET_PASSWORD_CODE
			reset_password_code.save()

			message_body = (
				f'Здравствуйте, {user.full_name}!\n'
				'Вы запросили восстановление пароля для вашего аккаунта на Sport WebSite.\n'  # noqa: E501
				'Для завершения процесса восстановления пароля, пожалуйста, используйте следующий код:\n'  # noqa: E501
				f'Восстановительный код: {reset_password_code.code}.\n'
				f'Срок действия кода: {reset_password_code.LIFETIME} минут.\n'
				f'Ссылка для ввода кода: http://127.0.0.1:5000/activate-code/{user.email}/1/\n'
				'Пожалуйста, введите этот код на странице восстановления пароля, '  # noqa: E501
				'а также укажите новый пароль.\n'
				'Если вы не запрашивали восстановление пароля, проигнорируйте это сообщение. '  # noqa: E501
				'Ваш пароль останется в безопасности.\n'
				'Если у вас возникли вопросы или проблемы, вы можете связаться с '  # noqa: E501
				'нами по одному из контаков в низу главной страницы сайта.\n'
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
					'subject': 'Сброс пароля',
					'message': message_body,
				}
			)
			channel.basic_publish(
				exchange='', routing_key='email_queue', body=message
			)

			connection.close()

			return Response({'unique_user': True}, status.HTTP_200_OK)

		return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


class ActivateCodeView(APIView):
	"""
	View for activation codes.
	"""

	def post(self, request: Request) -> Response:
		serializer: AuthCodeSerializer = AuthCodeSerializer(data=request.data)

		if serializer.is_valid():
			data = serializer.validated_data

			code_type = data.get('code_type')
			email = data.get('email')
			code = data.get('code')

			context_errors = {}

			is_error, errors = validate_email(email)
			if is_error:
				context_errors['email'] = errors

			is_error, errors = validate_code(code)
			if is_error:
				context_errors['email'] = errors

			if context_errors:
				return Response(
					{'errors': context_errors}, status.HTTP_400_BAD_REQUEST
				)

			if code_type == AuthCode.ACTIVATE_ACCOUNT_CODE:
				return ActivateAccountHandler.handle(data)

			elif code_type == AuthCode.RESET_PASSWORD_CODE:
				return RestorePasswordHandler.handle(data)

			return Response(
				{'errors': context_errors}, status.HTTP_400_BAD_REQUEST
			)

		return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


class ChangePasswordView(LoginRequiredMixin, views.View):
	"""
	View for user to change their password.
	"""

	def get(self, request: HttpRequest) -> HttpResponse:
		return render(
			request=request, template_name='auths/change-password.html'
		)

	def post(self, request: HttpRequest) -> HttpResponse:
		old_password: str = request.POST.get('old_password')
		new_password: str = request.POST.get('new_password')
		confirm_password: str = request.POST.get('confirm_password')

		current_user: User = request.user

		context_errors = []

		if not current_user.check_password(old_password):
			context_errors.append('Старый пароль не подходит.')

		if new_password != confirm_password:
			context_errors.append('Пароли не совпадают.')

		is_error, errors = validate_password(new_password)
		if is_error:
			context_errors.extend(errors)

		if context_errors:
			return render(
				request=request,
				template_name='auths/change-password.html',
				context={'errors': context_errors},
				status=400,
			)

		current_user.set_password(new_password)
		current_user.save()

		return redirect('profile/')
