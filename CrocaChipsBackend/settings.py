"""
Django settings for CrocaChipsBackend project.

Generated by 'django-admin startproject' using Django 5.2.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.2/ref/settings/
"""

import os
from pathlib import Path
from dotenv import load_dotenv
import pymysql
from datetime import timedelta
from corsheaders.defaults import default_headers

pymysql.install_as_MySQLdb()

load_dotenv()


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-5053a+qx6_p89*+abw%@ckgl^!4c+)a_#!dk&6e8#ra^qd9sf7'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['.vercel.app', 'localhost', '127.0.0.1']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Apps propias
    'Empleados',
    'Productos',
    'Clientes',
    'MovimientosAlmacen',
    'Ventas',

    # Librerias
    'corsheaders',
    'rest_framework',
    'rest_framework_simplejwt',
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'CrocaChipsBackend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'CrocaChipsBackend.wsgi.app'


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',  
        'NAME': 'bd_croca_chips',         
        'USER': 'root',         
        'PASSWORD': 'tArtcqaAiRUuFxZvUTiqjRNHYagEEdtR',  
        'HOST': 'maglev.proxy.rlwy.net',  
        'PORT': '43380', 
    }
}

CORS_ALLOWED_ORIGINS = [
    os.getenv("FRONTEND_URL", "http://localhost:5173"),
]

CORS_ALLOW_HEADERS = list(default_headers) + [
    'X-Requested-With',
    'Content-Type',
    'Authorization',
]

# Opcional para desarrollo (desactivalo en producción)
CORS_ALLOW_ALL_ORIGINS = True

# CONFIGURACION JWT
SIMPLE_JWT = {
      'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
}

SIMPLE_JWT = {
    # Duración del token de acceso (ej: 60 minutos)
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),

    # Duración del token de refresco (ej: 7 días)
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),

    # --- Otras configuraciones opcionales ---

    # Si quieres que los tokens de refresco roten (se emita uno nuevo cada vez que se usa)
    'ROTATE_REFRESH_TOKENS': False, # Cambia a True si lo deseas

    # Si quieres que el token de refresco antiguo se añada a la lista negra después de la rotación
    # Requiere que 'rest_framework_simplejwt.token_blacklist' esté en INSTALLED_APPS
    'BLACKLIST_AFTER_ROTATION': True,

    # Algoritmo de firma
    'ALGORITHM': 'HS256',

    # Clave secreta (por defecto usa settings.SECRET_KEY)
    # 'SIGNING_KEY': settings.SECRET_KEY,

    # Clave en el payload que identifica al usuario (por defecto 'user_id')
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
}


CORS_ALLOW_CREDENTIALS = True

# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
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
]


# Internationalization
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'es-us'

TIME_ZONE = 'America/La_Paz'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
