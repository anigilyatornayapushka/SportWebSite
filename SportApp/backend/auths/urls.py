from django.urls.conf import path

from .views import (
	RegistrationView,
	LoginView,
	RestorePasswordView,
	ChangePasswordView,
)


urlpatterns = (
	path('register/', RegistrationView.as_view(), name='register'),
	path('login/', LoginView.as_view(), name='login'),
	path(
		'restore-password/',
		RestorePasswordView.as_view(),
		name='restore-password',
	),
	path(
		'change-password/',
		ChangePasswordView.as_view(),
		name='change-password',
	),
)
