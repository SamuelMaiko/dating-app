from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent


SECRET_KEY = 'django-insecure-1-3az+0i^!n6l-ozsp!o4hbzgo-53zfc-=)g=-=+t^+tj0b5p3'


DEBUG=True
# DEBUG = os.environ.get('DEBUG', 'False').lower() in ['true', '1', 'yes']

ALLOWED_HOSTS=["maikomoringa.pythonanywhere.com", "localhost","127.0.0.1"]


INSTALLED_APPS = [
    'daphne',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'api',
    'userauth',
    'profiles',
    'chatapp',
    'matches',
    'groups',
    'appsettings',
    'discover',
    'rest_framework',
    'rest_framework.authtoken',
    'django_browser_reload',
    'drf_yasg',
    'corsheaders',
    'django_filters',
    'channels',
]

ASGI_APPLICATION='core.asgi.application'

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer",
    },
}
#CHANNEL_LAYERS = {
#    "default": {
#        "BACKEND": "channels_redis.core.RedisChannelLayer",
#        'CONFIG':{
#            'hosts':[('redis://default:KPdpgkIghcmYkAyfwlHufejWeqUDXsuy@viaduct.proxy.rlwy.net:13892')]
#            "hosts": [("127.0.0.1", 6379)],
#        },
#    },
#}

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django_browser_reload.middleware.BrowserReloadMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

CORS_ALLOW_ALL_ORIGINS = True


ROOT_URLCONF = 'core.urls'

INTERNAL_IPS=[
    "127.0.0.1",
]

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

WSGI_APPLICATION = 'core.wsgi.application'
 
DATABASES = {
    #Use this for development with SQLite
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
    
    #Use this for production with PostgreSQL
    
    # 'default': {
    #     'ENGINE': os.environ.get('DB_ENGINE', ''),
    #     'NAME': os.environ.get('DB_NAME', ''),
    #     'USER': os.environ.get('DB_USER', ''),
    #     'PASSWORD': os.environ.get('DB_PASSWORD', ''),
    #     'HOST': os.environ.get('DB_HOST', ''),
    #     'PORT': os.environ.get('DB_PORT', ''),
    # }
}


AUTH_USER_MODEL="userauth.CustomUser"

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


LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True



STATIC_URL = '/static/'
STATIC_ROOT=BASE_DIR / "app_static_files"

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'app_media'



DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ],
}


# email configs

# EMAIL_HOST = os.environ.get('EMAIL_HOST')
# EMAIL_BACKEND = os.environ.get('EMAIL_BACKEND')
# EMAIL_PORT = int(os.environ.get('EMAIL_PORT', 587))
# EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
# EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
# EMAIL_USE_TLS = os.environ.get('EMAIL_USE_TLS', 'True').lower() == 'true'
# EMAIL_USE_SSL = os.environ.get('EMAIL_USE_SSL', 'False').lower() == 'true'

EMAIL_BACKEND="django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST="smtp.gmail.com"
EMAIL_PORT=587
EMAIL_HOST_USER="sammymaiko721@gmail.com"
EMAIL_HOST_PASSWORD="mpjy fzjp eovw yobl"
EMAIL_USE_TLS=True
EMAIL_USE_SSL=False