import os
from pathlib import Path

from dotenv import load_dotenv

# ---BASE_DIR------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent.parent
# -----------------------------------------------------------------


# ---ENV-----------------------------------------------------------
load_dotenv(dotenv_path=BASE_DIR / ".env")
# -----------------------------------------------------------------


# ---SECURITY------------------------------------------------------
SECRET_KEY = os.getenv("SECRET_KEY")
DEBUG = bool(int(os.getenv("DEBUG", "0")))
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "*").split(",")
# -----------------------------------------------------------------


# ---CSRF---------------------------------------------------------
CSRF_TRUSTED_ORIGINS = os.getenv("CSRF_TRUSTED_ORIGINS", "https://localhost").split(",")
# ----------------------------------------------------------------


# ---Application definition---------------------------------------
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "whitenoise.middleware.WhiteNoiseMiddleware",
]

ROOT_URLCONF = 'config.urls'
# ----------------------------------------------------------------


# ---TEMPLATES----------------------------------------------------
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]
# ----------------------------------------------------------------


# ---WSGI---------------------------------------------------------
WSGI_APPLICATION = "config.wsgi.application"
# ----------------------------------------------------------------


# ---Auth---------------------------------------------------------
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
# ----------------------------------------------------------------


# ---Internationalization------------------------------------------
LANGUAGES = [
    ("fa", "Persian"),
    ("en", "English"),
    ("de", "German"),
]

LANGUAGE_CODE = 'en-us'


LOCALE_PATHS = [
    os.path.join(BASE_DIR, "locale"),
]

TIME_ZONE = 'UTC'

USE_I18N = True
USE_L10N = True
USE_TZ = False
# ----------------------------------------------------------------


# ---Static files-------------------------------------------------
STATIC_URL = "/static/"
STATIC_ROOT = os.getenv("STATIC_ROOT")

STATICFILES_DIRS = [
    BASE_DIR / os.getenv("STATICFILES_DIRS", "static/assets"),
]
# ----------------------------------------------------------------


# ---Media--------------------------------------------------------
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / os.getenv("MEDIA_ROOT", "static/media")
ENABLE_MEDIA_SERVE_IN_LOCAL = bool(int(os.getenv("ENABLE_MEDIA_SERVE_IN_LOCAL", 0)))
# ----------------------------------------------------------------


# ---Production whitenoise----------------------------------------
if int(os.getenv("ENABLE_WHITENOISE", default=0)):
    # Insert Whitenoise Middleware and set as StaticFileStorage
    MIDDLEWARE += [
        "whitenoise.middleware.WhiteNoiseMiddleware",
    ]
    STATICFILES_STORAGE = "whitenoise.storage.StaticFilesStorage"
# ----------------------------------------------------------------


# ---Default primary key field type------------------------------
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
# ---------------------------------------------------------------


# ---Redis-------------------------------------------------------
REDIS_CONFIG = {
    "DB": int(os.getenv("REDIS_DB", 0)),
    "HOST": os.getenv("REDIS_HOST", "localhost"),
    "PORT": os.getenv("REDIS_PORT", "6379"),
    "CHANNEL_NAME": os.getenv("REDIS_CHANNEL_NAME", "market_price"),
}
# ---------------------------------------------------------------
