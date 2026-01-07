import os
from .common import *

from dotenv import load_dotenv
load_dotenv()


DEBUG = True

SECRET_KEY= 'django-insecure-bjg!w$s&tdrt_8oba8n+v$j-i411@ft3%zi%2a5dnxx^%dj%y-'




import dj_database_url

DATABASES = {
    "default": dj_database_url.parse(os.environ.get("DATABASE_URL"), conn_max_age=600)
}
ALLOWED_HOSTS=['localhost','127.0.0.1']