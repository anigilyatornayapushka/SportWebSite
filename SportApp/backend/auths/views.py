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

import datetime

from services.email_sender import TextEmailSender
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
from .utils import datefy


class RegistrationView(views.View):
    """
    View for registration of user.
    """

    def get(self, request: HttpRequest) -> HttpResponse:
        return render(request=request,
                      template_name='auths/register.html', status=200)

    def post(self, request: HttpRequest) -> HttpResponse:
        context_errors = {}

        first_name: str = request.POST.get('first_name')
        last_name: str = request.POST.get('last_name')
        email: str = request.POST.get('email')
        password: str = request.POST.get('password')
        height: str = request.POST.get('height')
        birthday: str = request.POST.get('birthday')
        weight: str = request.POST.get('weight')
        gender: str = request.POST.get('gender')

        is_error, errors = validate_name(first_name)
        if is_error:
            context_errors['first_name'] = errors

        is_error, errors = validate_name(last_name)
        if is_error:
            context_errors['last_name'] = errors

        is_error, errors = validate_email(email)
        if is_error:
            context_errors['email'] = errors

        is_error, errors = validate_password(password)
        if is_error:
            context_errors['password'] = errors

        is_error, errors = validate_height(height)
        if is_error:
            context_errors['height'] = errors

        is_error, errors = validate_weight(weight)
        if is_error:
            context_errors['weight'] = errors

        datefy_birthday: datetime.date | str
        is_error, datefy_birthday = datefy(birthday)
        if is_error:
            context_errors['birthday'] = datefy_birthday
        else:
            birthday = datefy_birthday
            is_error, errors = validate_age(birthday)
            if is_error:
                context_errors['birthday'] = errors

        is_error, errors = validate_gender(gender)
        if is_error:
            context_errors['gender'] = errors

        is_error, errors = validate_unique_user(email)
        if is_error:
            context_errors['unique_user'] = False

        if errors:
            return render(request=request, template_name='auths/register.html',
                          context=context_errors, status=401)

        User.objects.create_user(email=email, password=password, first_name=first_name,
                            last_name=last_name, gender=int(gender), height=int(height),
                            weight=int(weight), birthday=birthday)

        return render(request=request, template_name='auths/register.html',
                      context={'unique_user': True}, status=201)

class LoginView(views.View):
    """
    View for login of user.
    """

    def get(self, request: HttpRequest) -> HttpResponse:
        return render(request=request,
                      template_name='auths/login.html')

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
            return render(request=request, template_name='auths/login.html',
                          context=authentication_errors, status=400)

        user: User | None = authenticate(request=request,
                                  email=email, password=password)

        if not user:
            return render(request=request, template_name='auths/login.html',
                          context={'user_not_found': 'Пользователь с таким '
                                   'логином или паролем не найден'}, status=400)

        login(request=request, user=user)

        return redirect('profile')

class RestorePasswordView(views.View):
    """
    View for user to restore their password.
    """
    def get(self, request: HttpRequest) -> HttpResponse:
        return render(request=request, template_name='auths/restore-password.html',
                      context={'stage': 1}, status=200)

    def post(self, request: HttpRequest) -> HttpResponse:
        stage: str = request.POST.get('stage')

        if stage == '1':
            email: str = request.POST.get('email')

            is_error, errors = validate_email(email)

            if is_error:
                return render(request=request, template_name='auths/restore-password.html',
                            context={'stage': 1, 'errors': errors}, status=400)

            user: User | None = User.objects.get_object_or_none(email=email)

            if not user:
                errors = ['Пользователь с данным email не найден.']
                return render(request=request, template_name='auths/restore-password.html',
                            context={'stage': 1, 'errors': errors}, status=400)

            reset_password_code = ResetPasswordCode(user=user)
            reset_password_code.save()

            message = (
                f'Здравствуйте, {user.full_name}!\n'
                'Вы запросили восстановление пароля для вашего аккаунта на Sport WebSite.\n'
                'Для завершения процесса восстановления пароля, пожалуйста, используйте следующий код:\n'
                f'Восстановительный код: {reset_password_code.code}.\n'
                f'Срок действия кода: {reset_password_code.LIFETIME} минут.\n'
                'Пожалуйста, введите этот код на странице восстановления пароля, '
                'а также укажите новый пароль.\n'
                'Если вы не запрашивали восстановление пароля, проигнорируйте это сообщение. '
                'Ваш пароль останется в безопасности.\n'
                'Если у вас возникли вопросы или проблемы, вы можете связаться с '
                'нами по одному из контаков в низу главной страницы сайта.\n'
                'С уважением,\n'
                'Команда Sport WebSite'
            )
            TextEmailSender(send_to=email, subject='Sport WebSite. Сброс пароля',
                            message=message).send_email()

            return render(request=request, template_name='auths/restore-password.html',
                          context={'stage': 2, 'email': email}, status=200)

        elif stage == '2':
            email: str = request.POST.get('email')
            reset_code: str = request.POST.get('reset_code')
            new_password: str = request.POST.get('new_password')
            confirm_password: str = request.POST.get('confirm_password')

            is_error, errors = validate_email(email)
            if is_error:
                context = {'stage': 2, 'errors': errors, 'email': email}
                return render(request=request, template_name='auths/restore-password.html',
                              context=context, status=400)

            is_error, errors = validate_password(new_password)
            if is_error:
                context = {'stage': 2, 'errors': errors, 'email': email}
                return render(request=request, template_name='auths/restore-password.html',
                              context=context, status=400)
            
            if new_password != confirm_password:
                context = {'stage': 2, 'errors': ['Пароли должны совпадать.'], 'email': email}
                return render(request=request, template_name='auths/restore-password.html',
                              context=context, status=400)

            user: User | None = User.objects.get_object_or_none(email=email)

            if not user:
                errors = ['Пользователь с данным email не найден.']
                return render(request=request, template_name='auths/restore-password.html',
                              context={'stage': 1, 'errors': errors}, status=400)
            
            active_codes: QuerySet[ResetPasswordCode] | None = \
                user.reset_password_codes.get_active_codes()
            correct_codes: QuerySet[ResetPasswordCode] | None = \
                active_codes.filter(code=reset_code)
            if not correct_codes.exists():
                errors = ['Данный код не существует.']
                return render(request=request, template_name='auths/restore-password.html',
                              context={'stage': 2, 'errors': errors}, status=400)

            user.set_password(new_password)
            user.save()
            login(request=request, user=user)

            return redirect('profile')

        else:
            errors = ['Стадий восстановления всего две.']
            return render(request=request, template_name='auths/restore-password.html',
                        context={'stage': 1, 'errors': errors}, status=400)



class ChangePasswordView(LoginRequiredMixin, views.View):
    """
    View for user to change their password.
    """
    def get(self, request: HttpRequest) -> HttpResponse:
        return render(request=request, template_name='auths/change-password.html')

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
            return render(request=request, template_name='auths/change-password.html',
                          context={'errors': context_errors}, status=400)

        current_user.set_password(new_password)
        current_user.save()

        return redirect('profile')
