"""
Django settings for TaskLedger backend project.
"""

from pathlib import Path
import environ
import os

# ---------------------------
# BASE DIRECTORY
# ---------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

# ---------------------------
# ENVIRONMENT VARIABLES
# ---------------------------
env = environ.Env(
    DEBUG=(bool, False)
)
# Read .env file located in backend/
environ.Env.read_env(os.path.join(BASE_DIR, ".env"))

# ---------------------------
# SECURITY
# ---------------------------
SECRET_KEY = env("SECRET_KEY")
DEBUG = env("DEBUG", default=True)
ALLOWED_HOSTS = []

# ---------------------------
# APPLICATION DEFINITION
# ---------------------------
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Third-party
    'corsheaders',
    'cloudinary',
    'cloudinary_storage',
    'rest_framework',
    'accounts',
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",  # must be at top
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "backend.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "backend.wsgi.application"

# ---------------------------
# DATABASE (PostgreSQL)
# ---------------------------
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": env("DB_NAME"),
        "USER": env("DB_USER"),
        "PASSWORD": env("DB_PASSWORD"),
        "HOST": env("DB_HOST", default="localhost"),
        "PORT": env("DB_PORT", default="5432"),
    }
}

# ---------------------------
# PASSWORD VALIDATION
# ---------------------------
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# ---------------------------
# INTERNATIONALIZATION
# ---------------------------
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# ---------------------------
# STATIC & MEDIA FILES
# ---------------------------
STATIC_URL = "/static/"
MEDIA_URL = "/media/"

# Cloudinary storage for media
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

# ---------------------------
# CORS
# ---------------------------
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
]

# ---------------------------
# DEFAULT AUTO FIELD
# ---------------------------
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# ----------------------------------
# CUSTOM USER Authentication Model 
# ----------------------------------
AUTH_USER_MODEL = "accounts.User"