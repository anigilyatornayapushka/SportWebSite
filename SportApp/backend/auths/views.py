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

import datetime

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
from .models import User
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
                          context=authentication_errors, status=401)

        user: User | None = authenticate(request=request,
                                  email=email, password=password)

        if not user:
            return render(request=request, template_name='auths/login.html',
                          context={'user_not_found': 'Пользователь с таким '
                                   'логином или паролем не найден'}, status=401)

        login(request=request, user=user)

        return redirect('profile')
