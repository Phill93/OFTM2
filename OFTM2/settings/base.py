'''Base Config for OFTM2'''
import os
import environ
on_heroku = False

if 'HEROKU' in os.environ:
    print("Heroku detected!")
    on_heroku = True

if on_heroku:
    import django_heroku

BASE_DIR = environ.Path(__file__) - 2


ENV = environ.Env(DEBUG=(bool, False), ALLOWED_HOSTS=(list, ["localhost", "127.0.0.1"]))

if not on_heroku:
    ENV.read_env(env_file=os.path.join(os.path.dirname(BASE_DIR), '.env'))

TMP_DIR = os.path.join(os.path.dirname(BASE_DIR), 'tmp')

if not on_heroku:
    SECRET_KEY = ENV('SECRET_KEY')

ALLOWED_HOSTS = ENV('ALLOWED_HOSTS')

DEBUG = ENV('DEBUG')
TEMPLATE_DEBUG = DEBUG

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'menu',
    'django_tables2',
    'OFTM2.apps.fencers_management',
    'OFTM2.apps.tournament_management',
    'OFTM2.apps.beamerManagement'
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

if DEBUG:
    INSTALLED_APPS.append('debug_toolbar')
    MIDDLEWARE.append('debug_toolbar.middleware.DebugToolbarMiddleware')
    INTERNAL_IPS = ALLOWED_HOSTS

ROOT_URLCONF = 'OFTM2.urls'
LOGOUT_REDIRECT_URL = 'portal'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, "templates"),
        ],
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

WSGI_APPLICATION = 'OFTM2.wsgi.application'

if on_heroku:
    DATABASES = {
        'default': ENV.db('HEROKU_POSTGRESQL_PURPLE_URL')
    }
else:
    DATABASES = {
        'default': ENV.db()
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

LANGUAGE_CODE = 'de-de'

TIME_ZONE = 'Europe/Berlin'

USE_I18N = True

USE_L10N = True

USE_TZ = True


STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

STATICFILES_DIRS = [
    os.path.join(os.path.dirname(BASE_DIR), "dist"),
]

if on_heroku:
    # Activate Django-Heroku.
    django_heroku.settings(locals())