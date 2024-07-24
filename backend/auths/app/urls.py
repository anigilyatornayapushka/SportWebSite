from django.urls import path

from .views import (
    RegistrationView,
    RestorePasswordView,
    ActivateCodeView,
)


urlpatterns = (
    path('register/', RegistrationView.as_view()),
    path('restore-password/', RestorePasswordView.as_view()),
    path('activate-code/', ActivateCodeView.as_view()),
)
