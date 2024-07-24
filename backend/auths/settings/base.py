from pathlib import Path
import sys

import decouple


BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(BASE_DIR)

SECRET_KEY = decouple.config('SECRET_KEY', cast=str)

DEBUG = decouple.config('DEBUG', cast=bool)

AUTH_USER_MODEL = 'app.User'

ALLOWED_HOSTS = ('*',)

CORS_ALLOWED_ORIGINS = (
    'http://localhost:5000',
    'http://127.0.0.1:5000',
)

INSTALLED_APPS = (
	'django.contrib.admin',
	'django.contrib.auth',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
	'django.contrib.messages',
	'django.contrib.staticfiles',
	'rest_framework',
	'corsheaders',
	'app',
)

MIDDLEWARE = (
	'django.middleware.security.SecurityMiddleware',
	'django.contrib.sessions.middleware.SessionMiddleware',
	'django.middleware.common.CommonMiddleware',
	'corsheaders.middleware.CorsMiddleware',
	'django.contrib.auth.middleware.AuthenticationMiddleware',
	'django.contrib.messages.middleware.MessageMiddleware',
	'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'settings.urls'

TEMPLATES = (
	{
		'BACKEND': 'django.template.backends.django.DjangoTemplates',
		'DIRS': (),
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
		'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',  # noqa: E501
	},
	{
		'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',  # noqa: E501
	},
	{
		'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',  # noqa: E501
	},
	{
		'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',  # noqa: E501
	},
)

LANGUAGE_CODE = 'ru-RU'

TIME_ZONE = 'Asia/Almaty'

USE_I18N = True

USE_TZ = True

STATIC_URL = '/static/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
