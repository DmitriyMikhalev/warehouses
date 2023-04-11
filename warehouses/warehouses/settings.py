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
    'warehouse.apps.WarehouseConfig',
    'users.apps.UsersConfig'
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

TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates')

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATES_DIR],
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

STATIC_URL = '/static/'

MEDIA_URL = '/media/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

MIN_ARTICLE_NUMBER = 10000

MAX_NAME_LENGTH = 50

MAX_PRODUCT_NAME_LENGTH = 100

MAX_EMAIL_LENGTH = 30

MAX_VEHICLE_BRAND_LENGTH = 30

VIN_LENGTH = 17

MAX_ADDRESS_LENGTH = 50

MAX_WAREHOUSE_NAME_LENGTH = 50

MAX_SHOP_NAME_LENGTH = MAX_WAREHOUSE_NAME_LENGTH

TIMEZONE_OFFSET = 5.0

ORDER_DAYS_MIN_OFFSET = 1

ORDER_DAYS_MAX_OFFSET = 90

LIST_PER_PAGE = 30

QUERY_1_DESCRIPTION = 'Получить имена и электронные адреса всех владельцев складов, машин или магазинов.'

QUERY_2_DESCRIPTION = 'Получить марки и грузоподъемность всех машин с грузоподъемностью менее 15 тонн.'

QUERY_3_DESCRIPTION = 'Получить название, адрес и вместительность склада с наибольшей вместительностью в тоннах.'

QUERY_4_DESCRIPTION = 'Получить названия, адреса, время начала и конца поставки товаров на склады на определенный день в UTC.'

QUERY_5_DESCRIPTION = 'Получить имя и фамилию владельца и суммарную вместимость в тоннах его складов для конкретного владельца.'

QUERY_6_DESCRIPTION = 'Получить адреса складов, в которые осуществляют транзит машины определенного владельца в определенный день в UTC.'

QUERY_7_DESCRIPTION = 'Получить список машин (марка и грузоподъемность) в порядке убывания грузоподъемности, везущих товары в магазин не позднее 17:00 UTC конкретного дня.'

QUERY_8_DESCRIPTION = 'Получить адреса складов с минимальным числом заказов (магазинами) на определенный день в UTC.'

QUERY_9_DESCRIPTION = 'Получить количество поставок на склады длительностью более 3 часов на определенный день в UTC.'

QUERY_10_DESCRIPTION = 'Получить наименование, артикул и количество товаров, преобладающих по количеству (в тоннах) на определенном складе.'

LOGIN_URL = 'users:login'

LOGIN_REDIRECT_URL = 'warehouses:index'

AUTH_USER_MODEL = 'users.User'
