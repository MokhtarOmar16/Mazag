import os
import dj_database_url
from .common import *


DEBUG = False

SECRET_KEY = os.environ.get("SECRET_KEY")

ALLOWED_HOSTS = ["*"]

INSTALLED_APPS += [
    'cloudinary_storage',
    'cloudinary',
]

CLOUDINARY_STORAGE = {
    'CLOUD_NAME': os.getenv("CLOUD_STORAGE_NAME"),
    'API_KEY': os.getenv("CLOUD_API_KEY"),
    'API_SECRET': os.getenv("CLOUD_API_SECRET"),
}

DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'
DATABASES = {
    'default': dj_database_url.config()
}