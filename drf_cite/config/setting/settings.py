from .base import *

BASE_DIR = Path(__file__).resolve().parent.parent.parent

SECRET_KEY = config('SECRET_KEY')

# ALLOWED_HOSTS = ("sr.horizon-logistics.co", "167.99.243.166", 'localhost', "127.0.0.1")

ALLOWED_HOSTS = ("*",)

AUTH_USER_MODEL = 'users.User'

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": config('DB_NAME'),
        'USER': config('DB_USER'),
        "PASSWORD": config('DB_PASS'),
        'HOST': config('DB_HOST'),
        'PORT': 5432,
    }
}

# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.sqlite3",
#         "NAME": BASE_DIR / "db.sqlite3",
#     }
# }

STATIC_URL = "/users/back-static/"
STATIC_ROOT = os.path.join(BASE_DIR, "back-static")

MEDIA_URL = '/users/back-media/'
MEDIA_ROOT = os.path.join(BASE_DIR, "back-media")

# CSRF_TRUSTED_ORIGINS = ["https://sr.horizon-logistics.co", "http://167.99.243.166",
#                         "http://localhost:8003", "http://192.168.138.58:8501",
#                         "https://sr.horizon-logistics.co/streamlit/"]

# CORS_ALLOWED_ORIGINS = ["http://localhost:3000", "http://127.0.0.1:3000", "https://horizon-logistics.co"]

CORS_ALLOW_ALL_ORIGINS = True

CORS_ALLOW_CREDENTIALS = True


CORS_ALLOW_METHODS = [
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
    "HEAD",
]

CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
]

