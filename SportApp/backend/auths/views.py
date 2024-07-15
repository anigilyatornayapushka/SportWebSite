from django.shortcuts import render
from django import views
from django.http import (
    HttpRequest,
    HttpResponse,
)


class RegistrationView(views.View):
    """
    View for registration of user.
    """

    def get(self, request: HttpRequest) -> HttpResponse:
        return render(request=request,
                      template_name='auths/register.html')


class LoginView(views.View):
    """
    View for login of user.
    """

    def get(self, request: HttpRequest) -> HttpResponse:
        return render(request=request,
                      template_name='auths/login.html')
