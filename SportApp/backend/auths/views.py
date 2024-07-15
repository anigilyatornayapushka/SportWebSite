from django.shortcuts import render
from django import views
from django.http import (
    HttpRequest,
    HttpResponse,
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
from .models import User


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
        age: str = request.POST.get('age')
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

        is_error, errors = validate_age(age)
        if is_error:
            context_errors['age'] = errors

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
                            weight=int(weight), age=int(age))

        return render(request=request, template_name='auths/register.html',
                      context={'unique_user': True}, status=201)

class LoginView(views.View):
    """
    View for login of user.
    """

    def get(self, request: HttpRequest) -> HttpResponse:
        return render(request=request,
                      template_name='auths/login.html')
