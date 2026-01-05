import os
from .common import *

from dotenv import load_dotenv
load_dotenv()


DEBUG = True

SECRET_KEY= 'django-insecure-bjg!w$s&tdrt_8oba8n+v$j-i411@ft3%zi%2a5dnxx^%dj%y-'



DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ.get('DB_NAME', 'storefront'),
        'USER': os.environ.get('DB_USER', 'root'),
        'PASSWORD': os.environ.get('DB_PASSWORD', ''),
        'HOST': os.environ.get('DB_HOST', '127.0.0.1'),
        'PORT': os.environ.get('DB_PORT', '3306'),
    }
}
