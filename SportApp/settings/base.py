from pathlib import Path
import sys
import os

import decouple


BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(BASE_DIR)
sys.path.append(os.path.join(BASE_DIR, 'backend'))

SECRET_KEY = decouple.config('SECRET_KEY', cast=str)

DEBUG = decouple.config('DEBUG', cast=bool)

AUTH_USER_MODEL = 'auths.User'

LOGIN_URL = 'login'

ALLOWED_HOSTS = ('*',)

DJANGO_APPS = (
	'django.contrib.admin',
	'django.contrib.auth',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
	'django.contrib.messages',
	'django.contrib.staticfiles',
)

CUSTOM_APPS = (
	'auths',
	'abstracts',
	'information_pages',
)

INSTALLED_APPS = DJANGO_APPS + CUSTOM_APPS

MIDDLEWARE = (
	'django.middleware.security.SecurityMiddleware',
	'django.contrib.sessions.middleware.SessionMiddleware',
	'django.middleware.common.CommonMiddleware',
	'django.middleware.csrf.CsrfViewMiddleware',
	'django.contrib.auth.middleware.AuthenticationMiddleware',
	'django.contrib.messages.middleware.MessageMiddleware',
	'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'settings.urls'

TEMPLATES = (
	{
		'BACKEND': 'django.template.backends.django.DjangoTemplates',
		'DIRS': ('frontend/templates',),
		'APP_DIRS': True,
		'OPTIONS': {
			'context_processors': (
				'django.template.context_processors.debug',
				'django.template.context_processors.request',
				'django.contrib.auth.context_processors.auth',
				'django.contrib.messages.context_processors.messages',
			),
		},
	},
)

WSGI_APPLICATION = 'settings.wsgi.application'

DATABASES = {
	'default': {
		'ENGINE': 'django.db.backends.sqlite3',
		'NAME': BASE_DIR / 'db.sqlite3',
	}
}

AUTH_PASSWORD_VALIDATORS = (
	{
		'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
	},
	{
		'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
	},
	{
		'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
	},
	{
		'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
	},
)

LANGUAGE_CODE = 'ru-RU'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

STATIC_URL = '/static/'
STATICFILES_DIRS = (BASE_DIR / 'frontend/static',)

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# EMAIL-HOST
# ---------------------------------------------------------------------

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST = decouple.config('EMAIL_HOST', cast=str)
EMAIL_HOST_USER = decouple.config('EMAIL_HOST_USER', cast=str)
EMAIL_HOST_PASSWORD = decouple.config('EMAIL_HOST_PASSWORD', cast=str)
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
