import os
from pathlib import Path
# from dotenv import load_dotenv
# load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

# =========================
# Secret Key & Debug
# =========================
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'django-insecure-your-secret-key')

# Detect if running on Render
RENDER_ENV = os.environ.get('RENDER', None)
if RENDER_ENV:
    DEBUG = False
    ALLOWED_HOSTS = ['groceryshop-74h8.onrender.com']
else:
    DEBUG = True
    ALLOWED_HOSTS = ['127.0.0.1', 'localhost']

# =========================
# Application Definition
# =========================
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'GroceryShopApp',  # your app
    'django_extensions',  # optional, helpful in dev
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # static files
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'GroceryShop.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # templates folder
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# RAZORPAY_KEY_ID = os.getenv('rzp_live_RZLWxbScWFFLQq')
# RAZORPAY_KEY_SECRET = os.getenv('YJ6nzXvLPc32fmyYL75AMkrU')


RAZORPAY_KEY_ID = "rzp_live_RZLWxbScWFFLQq"
RAZORPAY_KEY_SECRET = "YJ6nzXvLPc32fmyYL75AMkrU"

WSGI_APPLICATION = 'GroceryShop.wsgi.application'

# =========================
# Database
# =========================
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# =========================
# Password Validators
# =========================
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# =========================
# Localization
# =========================
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kolkata'
USE_I18N = True
USE_TZ = True

# =========================
# Static & Media Files
# =========================
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR /'staticfiles'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# =========================
# Security for HTTPS
# =========================
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SESSION_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_SECURE = not DEBUG

# =========================
# Default Primary Key
# =========================
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
