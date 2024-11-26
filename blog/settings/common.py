"""
Django settings for blog project.

Generated by 'django-admin startproject' using Django 5.1.1.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from datetime import timedelta
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    'whitenoise.runserver_nostatic',
    'drf_spectacular',
    
    #pkgs for debugging
    'debug_toolbar',
    
    # pkgs for rest 
    'rest_framework',
    'rest_framework.authtoken',
    'djoser',
    'corsheaders',
    'cloudinary_storage',
    'cloudinary',
    
    #custom app 
    'users',
    'posts'
    
    
]



MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    "whitenoise.middleware.WhiteNoiseMiddleware",
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'blog.urls'

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

WSGI_APPLICATION = 'blog.wsgi.application'



# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


INTERNAL_IPS = [
    '127.0.0.1',
]
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATICFILES_STORAGE="whitenoise.storage.CompressedManifestStaticFilesStorage"

# MEDIA_URL = 'media/'
# MEDIA_ROOT = "/media/"

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'users.User'
AUTHENTICATION_BACKENDS = [
    'users.backends.EmailBackend',
]


REST_FRAMEWORK = {
    'COERCE_DECIMAL_TO_STRING': False,
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 20
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=1) ,
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    'AUTH_HEADER_TYPES': ('JWT',),
    
}
SPECTACULAR_SETTINGS = {
    'TITLE': 'Mazag APIs',
    'DESCRIPTION': '''Mazag is an innovative platform that aligns with your current mood, offering a personalized experience through music, events, activities, and content recommendations. Whether you're seeking relaxation, inspiration, or excitement, Mazag curates suggestions and tools based on how you feel, helping you make the most of every moment. With social sharing and mental well-being features, Mazag creates a space where you can connect, express yourself, and discover new ways to elevate your day.''',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': 0,
}



DJOSER = {
    'TOKEN_MODEL': None, 

}


CORS_ALLOWED_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True

CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "https://only-freinds.vercel.app"
]


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'  
EMAIL_PORT = 587
EMAIL_USE_TLS = True

EMAIL_HOST_USER = os.getenv('GMAIL_USER')
EMAIL_HOST_PASSWORD = os.getenv('GMAIL_APP_PASSWORD')

DEFAULT_FROM_EMAIL = EMAIL_HOST_USER



CLOUDINARY_STORAGE = {
    'CLOUD_NAME': "dp3aijobb",
    'API_KEY': "251497421882178",
    'API_SECRET':"dmxuY3q5NhJLSeIsE-lx9iWT19c",
}
MEDIA_URL = '/media/'  # or any prefix you choose
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'
