import os

from pathlib import Path

from django.contrib.messages import constants as message_constants

from fatama.cast import string_to_boolean

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ["SECRET_KEY"]

DEBUG = string_to_boolean(os.getenv("DEBUG", "false"))

ALLOWED_HOSTS = ["127.0.0.1", "localhost"] + [
    host
    for host in (
        os.getenv("ALLOWED_HOSTS", "www.fatama2024.de").replace(" ", "").split(",")
    )
    if host
]


# Application definition

SITE_ID = 1

INSTALLED_APPS = [
    "accounts",
    "congresses",
    "excursions",
    "workshops",
    "fontawesomefree",
    "django.contrib.flatpages",
    "django.contrib.sites",
    "django.forms",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "fatama.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            BASE_DIR / "fatama" / "templates",
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "congresses.context_processors.congresses",
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
            "libraries": {
                "markdown": "fatama.templatetags.markdown",
            },
        },
    },
]

WSGI_APPLICATION = "fatama.wsgi.application"


# Database

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("DB_NAME", "fatama"),
        "USER": os.getenv("DB_USER", "fatama"),
        "PASSWORD": os.getenv("DB_PASSWORD"),
        "HOST": os.getenv("DB_HOST", "127.0.0.1"),
        "PORT": os.getenv("DB_PORT", "5432"),
    }
}


# Password validation

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization

LANGUAGE_CODE = "de-de"

TIME_ZONE = "Europe/Berlin"

USE_I18N = False

USE_TZ = True


# Static files (CSS, JavaScript, Images)

STATIC_ROOT = os.getenv("STATIC_ROOT", str((BASE_DIR / "static").absolute()))

STATIC_URL = "static/"

STATICFILES_DIRS = [
    BASE_DIR / "fatama" / "static",
]


# Media storage

MEDIA_ROOT = os.getenv("MEDIA_ROOT", str((BASE_DIR / "media").absolute()))

MEDIA_URL = "media/"


# Default primary key field type

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# Registration

INVITE_TOKEN_LENGTH = 10  # Bytes

INVITE_EXPIRATION = 10  # Days


# E-Mail

EMAIL_HOST = os.getenv("EMAIL_HOST", "smtp.postmarkapp.com")

EMAIL_PORT = os.getenv("EMAIL_PORT", "587")

POSTMARK_API_TOKEN = os.getenv("POSTMARK_API_TOKEN")

EMAIL_HOST_USER = os.getenv("EMAIL_USER")

EMAIL_HOST_PASSWORD = os.getenv("EMAIL_PASSWORD")

EMAIL_USE_TLS = True

DEFAULT_FROM_EMAIL = "hello@fatama2024.de"

SERVER_EMAIL = "support@fatama2024.de"


# Messages

MESSAGE_LEVEL = getattr(message_constants, os.getenv("MESSAGE_LEVEL", "INFO"))

MESSAGE_TAGS = {
    message_constants.DEBUG: "",
    message_constants.INFO: "is-info",
    message_constants.SUCCESS: "is-success",
    message_constants.WARNING: "is-warning",
    message_constants.ERROR: "is-danger",
}


# Forms

FORM_RENDERER = "fatama.forms.BulmaFormRenderer"


# Logging

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{asctime} {levelname:8} {message}",
            "style": "{",
        },
        "simple": {
            "format": "{message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "level": "INFO",
            "formatter": "simple",
            "class": "logging.StreamHandler",
        },
        "file": {
            "level": "INFO",
            "formatter": "verbose",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": BASE_DIR / "django.log",
            "maxBytes": 10**7,  # 10 MB
            "backupCount": 1,
        },
        "mail": {
            "level": "ERROR",
            "class": "django.utils.log.AdminEmailHandler",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["console", "file"],
            "propagate": True,
        },
        "django.requests": {
            "handlers": ["mail"],
            "level": "ERROR",
            "propagate": False,
        },
    },
}
