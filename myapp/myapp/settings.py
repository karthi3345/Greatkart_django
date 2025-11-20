"""
Django settings for myapp project.
"""

from pathlib import Path
from django.utils.translation import gettext_lazy as _

# ---------------------------------------------------------
# BASE DIRECTORY
# ---------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

# ---------------------------------------------------------
# SECURITY
# ---------------------------------------------------------

SECRET_KEY = 'django-insecure-amt_!c74uennxl-56xvdet7r0s&^6l9(_tdll^pe_^)^nc_1s('
DEBUG = True
ALLOWED_HOSTS = []

# ---------------------------------------------------------
# INSTALLED APPS
# ---------------------------------------------------------

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Your apps
    'myapp',
    'category',
    'accounts',
    'store',
]

# ---------------------------------------------------------
# MIDDLEWARE (Correct order!)
# ---------------------------------------------------------

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",

    # Important — LocaleMiddleware MUST be after SessionMiddleware
    "django.middleware.locale.LocaleMiddleware",

    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# ---------------------------------------------------------
# URL + WSGI
# ---------------------------------------------------------

ROOT_URLCONF = 'myapp.urls'
WSGI_APPLICATION = 'myapp.wsgi.application'

# ---------------------------------------------------------
# TEMPLATES
# ---------------------------------------------------------

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'templates',
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.template.context_processors.i18n',   # REQUIRED
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',

                # Custom processor
                'category.context_processors.menu_links',
            ],
        },
    },
]

# ---------------------------------------------------------
# AUTH USER
# ---------------------------------------------------------

AUTH_USER_MODEL = 'accounts.account'

# ---------------------------------------------------------
# DATABASE
# ---------------------------------------------------------

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'ecommerces_db',
        'USER': 'postgres',
        'PASSWORD': 'admin123',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# ---------------------------------------------------------
# PASSWORD RULES
# ---------------------------------------------------------

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ---------------------------------------------------------
# INTERNATIONALIZATION (FULLY CORRECTED)
# ---------------------------------------------------------

LANGUAGE_CODE = 'en'   # Default language

LANGUAGES = [
    ('en', _('English')),
    ('ta', _('Tamil')),
    ('hi', _('Hindi')),
    ('te', _('Telugu')),
    ('kn', _('Kannada')),
]

LOCALE_PATHS = [
    BASE_DIR / 'locale',
]

USE_I18N = True
USE_TZ = True
TIME_ZONE = 'UTC'

# REQUIRED: Without this, la

#STATIC FILES (CSS, JS, IMAGES)
# ---------------------------------------------
STATIC_URL = '/static/'

STATICFILES_DIRS = [
    BASE_DIR / 'myapp' / 'static',
]

STATIC_ROOT = BASE_DIR / 'staticfiles'

# ---------------------------------------------
# MEDIA FILES (UPLOADED IMAGES)
# ---------------------------------------------
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'