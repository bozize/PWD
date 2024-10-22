import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Security settings
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'default_secret_key')  # Use an environment variable
DEBUG = os.environ.get('DEBUG', 'False') == 'True'  # Convert the string value to boolean

# Allowed hosts for production
ALLOWED_HOSTS = ['safestep-frfda9eqdkg2cnh7.centralindia-01.azurewebsites.net']

# Azure Computer Vision settings
AZURE_COMPUTER_VISION_ENDPOINT = os.environ.get('AZURE_COMPUTER_VISION_ENDPOINT', 'https://default-endpoint.com/')
AZURE_COMPUTER_VISION_KEY = os.environ.get('AZURE_COMPUTER_VISION_KEY', 'default_key')

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'rest_framework',
    'pwdapp',
]

CORS_ALLOW_ALL_ORIGINS = True

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'PWD.urls'

CSRF_TRUSTED_ORIGINS = [
    'https://safestep-frfda9eqdkg2cnh7.centralindia-01.azurewebsites.net',
]


WSGI_APPLICATION = 'PWD.wsgi.application'

# Database settings
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('dbname'),
        'USER': os.getenv('user'),
        'PASSWORD': os.getenv('password'),
        'HOST': os.getenv('host'),
        'PORT': os.getenv('port'),
        'OPTIONS': {
            'sslmode': 'require',  # Required for Azure PostgreSQL
        },
    }
}



# Password validation
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





DATA_UPLOAD_MAX_MEMORY_SIZE = 52428800 

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True


STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / "staticfiles"

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')  
MEDIA_URL = '/media/'
