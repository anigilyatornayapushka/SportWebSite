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
from django.db.models.query import QuerySet

from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

import pika
import json


from .serializers import (
	RegistrationSerializer,
)
from .validators import (
	validate_email,
	validate_unique_user,
	validate_gender,
	validate_name,
	validate_password,
	validate_age,
	validate_height,
	validate_weight,
)
from .models import (
	User,
	ResetPasswordCode,
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

			is_error, errors = validate_unique_user(data.get('email'))
			if is_error:
				context_errors['unique_user'] = False

			if context_errors:
				return Response(
					{'error': context_errors}, status.HTTP_401_UNAUTHORIZED
				)

			serializer.save()

			return Response({'unique_user': True}, status.HTTP_201_CREATED)

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


class RestorePasswordView(views.View):
	"""
	View for user to restore their password.
	"""

	def get(self, request: HttpRequest) -> HttpResponse:
		return render(
			request=request,
			template_name='auths/restore-password.html',
			context={'stage': 1},
			status=200,
		)

	def post(self, request: HttpRequest) -> HttpResponse:
		stage: str = request.POST.get('stage')

		if stage == '1':
			email: str = request.POST.get('email')

			is_error, errors = validate_email(email)

			if is_error:
				return render(
					request=request,
					template_name='auths/restore-password.html',
					context={'stage': 1, 'errors': errors},
					status=400,
				)

			user: User | None = User.objects.filter(email=email)

			if not user:
				errors = ['Пользователь с данным email не найден.']
				return render(
					request=request,
					template_name='auths/restore-password.html',
					context={'stage': 1, 'errors': errors},
					status=400,
				)

			reset_password_code = ResetPasswordCode(user=user)
			reset_password_code.save()

			message_body = (
				f'Здравствуйте, {user.full_name}!\n'
				'Вы запросили восстановление пароля для вашего аккаунта на Sport WebSite.\n'  # noqa: E501
				'Для завершения процесса восстановления пароля, пожалуйста, используйте следующий код:\n'  # noqa: E501
				f'Восстановительный код: {reset_password_code.code}.\n'
				f'Срок действия кода: {reset_password_code.LIFETIME} минут.\n'
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

			return render(
				request=request,
				template_name='auths/restore-password.html',
				context={'stage': 2, 'email': email},
				status=200,
			)

		elif stage == '2':
			email: str = request.POST.get('email')
			reset_code: str = request.POST.get('reset_code')
			new_password: str = request.POST.get('new_password')
			confirm_password: str = request.POST.get('confirm_password')

			is_error, errors = validate_email(email)
			if is_error:
				context = {'stage': 2, 'errors': errors, 'email': email}
				return render(
					request=request,
					template_name='auths/restore-password.html',
					context=context,
					status=400,
				)

			is_error, errors = validate_password(new_password)
			if is_error:
				context = {'stage': 2, 'errors': errors, 'email': email}
				return render(
					request=request,
					template_name='auths/restore-password.html',
					context=context,
					status=400,
				)

			if new_password != confirm_password:
				context = {
					'stage': 2,
					'errors': ['Пароли должны совпадать.'],
					'email': email,
				}
				return render(
					request=request,
					template_name='auths/restore-password.html',
					context=context,
					status=400,
				)

			user: User | None = User.objects.filter(email=email)

			if not user:
				errors = ['Пользователь с данным email не найден.']
				return render(
					request=request,
					template_name='auths/restore-password.html',
					context={'stage': 1, 'errors': errors},
					status=400,
				)

			active_codes: QuerySet[ResetPasswordCode] | None = (
				user.reset_password_codes.get_active_codes()
			)
			correct_codes: QuerySet[ResetPasswordCode] | None = (
				active_codes.filter(code=reset_code)
			)
			if not correct_codes.exists():
				errors = ['Данный код не существует.']
				return render(
					request=request,
					template_name='auths/restore-password.html',
					context={'stage': 2, 'errors': errors},
					status=400,
				)

			user.set_password(new_password)
			user.save()
			login(request=request, user=user)

			return redirect('profile/')

		else:
			errors = ['Стадий восстановления всего две.']
			return render(
				request=request,
				template_name='auths/restore-password.html',
				context={'stage': 1, 'errors': errors},
				status=400,
			)


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
