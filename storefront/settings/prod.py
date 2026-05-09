import os
from pathlib import Path
from dotenv import load_dotenv
import dj_database_url
from .common import *


BASE_DIR = Path(__file__).resolve().parent.parent.parent
load_dotenv(os.path.join(BASE_DIR, ".env"))

DATABASES = {
    "default": dj_database_url.parse(os.environ.get("DATABASE_URL"), conn_max_age=600)
}

SECRET_KEY = os.environ.get("SECRET_KEY")
DEBUG = os.environ.get("DEBUG", "False") == "True"

ALLOWED_HOSTS = [
    "nepecom.onrender.com",  # your Render URL
    "www.nepecom.onrender.com",
    "http://localhost:5173",
    
    'localhost',
    '127.0.0.1',
]
CORS_ALLOW_ALL_ORIGINS = True
print(os.environ.get("DATABASE_URL"))


#email host 
EMAIL_BACKEND='django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD")
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
