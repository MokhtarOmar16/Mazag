from .common import *


SECRET_KEY = 'django-insecure-s!r(5-i1@cc8+bs0(a#q44j+dzryt9q^*qrd*os5eu(2@0^&$-'
DEBUG = True



# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}