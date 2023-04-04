from pathlib import Path
import os
from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent.parent

DOTENV_PATH = BASE_DIR.parent.joinpath('.env')

load_dotenv(dotenv_path=DOTENV_PATH)

SECRET_KEY = os.getenv('DJANGO_KEY')

DEBUG = True

ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1'
]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'warehouse.apps.WarehouseConfig'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'warehouses.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'warehouses.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': os.getenv(
            key='DB_ENGINE',
            default='django.db.backends.postgresql'
        ),
        'NAME': os.getenv(
            key='DB_NAME',
            default='db_name'
        ),
        'USER': os.getenv(
            key='DB_USER',
            default='db_user'
        ),
        'PASSWORD': os.getenv(
            key='DB_PASSWORD',
            default='password'
        ),
        'HOST': os.getenv(
            key='DB_HOST',
            default='database_host|container_name'
        ),
        'PORT': os.getenv(
            key='DB_PORT',
            default='5432'
        )
    }
}

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

LANGUAGE_CODE = 'ru'

TIME_ZONE = 'Asia/Yekaterinburg'

USE_I18N = True

USE_TZ = True

STATIC_URL = 'static/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

MIN_ARTICLE_NUMBER = 10000

MAX_NAME_LENGTH = 30

MAX_PRODUCT_NAME_LENGTH = 100

MAX_EMAIL_LENGTH = MAX_NAME_LENGTH

MAX_VEHICLE_BRAND_LENGTH = MAX_NAME_LENGTH

VIN_LENGTH = 17

MAX_ADDRESS_LENGTH = 50

MAX_WAREHOUSE_NAME_LENGTH = 50

MAX_SHOP_NAME_LENGTH = MAX_WAREHOUSE_NAME_LENGTH

TIMEZONE_OFFSET = 5.0

ORDER_DAYS_MIN_OFFSET = 1

ORDER_DAYS_MAX_OFFSET = 90
