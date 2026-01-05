import os
from .common import *
import dj_database_url

DEBUG = False

# Secret key from Render environment
SECRET_KEY = os.environ.get("SECRET_KEY")

# Allow all hosts for Render
ALLOWED_HOSTS = ["*"]

# Database from Render's DATABASE_URL
DATABASES = {
    "default": dj_database_url.config(
        default=os.environ.get("DATABASE_URL"),
        conn_max_age=600,
    )
}

# Static files settings for Render


# Optional: whitenoise for serving static files
MIDDLEWARE.insert(1, "whitenoise.middleware.WhiteNoiseMiddleware")
