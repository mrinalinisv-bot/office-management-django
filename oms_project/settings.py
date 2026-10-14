import os
from pathlib import Path

import dj_database_url


BASE_DIR = Path(__file__).resolve().parent.parent


# Security
SECRET_KEY = os.environ.get(
    "SECRET_KEY",
    "django-insecure-local-development-key-change-before-production",
)

DEBUG = os.environ.get("DEBUG", "True").strip().lower() in {
    "true", "1", "yes"
}


# Accept all hosts so Render subdomains, custom domains, and proxies work seamlessly
ALLOWED_HOSTS = ["*"]

# Trust Render reverse proxy for HTTPS detection
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")




# Applications
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "core",
]


# Middleware
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


ROOT_URLCONF = "oms_project.urls"


# Templates
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "core.context_processors.oms_global_context",
            ],
        },
    },
]


WSGI_APPLICATION = "oms_project.wsgi.application"


# Database
DATABASE_URL = os.environ.get("DATABASE_URL")
USE_SQLITE = os.environ.get("USE_SQLITE", "false").strip().lower() in {
    "true", "1", "yes"
}

if USE_SQLITE:
    # Explicit SQLite mode
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

elif DATABASE_URL:
    # Hosted PostgreSQL (Render PostgreSQL, Neon, Supabase, etc.)
    # Do not force sslmode=require for internal connections (dpg-..., .internal, localhost)
    is_internal = any(k in DATABASE_URL for k in ["localhost", "127.0.0.1", "dpg-", ".internal"])
    ssl_require = False if is_internal else (os.environ.get("DB_SSL_REQUIRE", "false").lower() in ("true", "1", "yes"))
    DATABASES = {
        "default": dj_database_url.parse(
            DATABASE_URL,
            conn_max_age=600,
            ssl_require=ssl_require,
        )
    }

elif os.environ.get("RENDER"):
    # Running on Render without a PostgreSQL DATABASE_URL:
    # Auto-fallback to SQLite so the app NEVER fails to deploy!
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

else:
    # Local development: default to local PostgreSQL oms_db
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": os.environ.get("DB_NAME", "oms_db"),
            "USER": os.environ.get("DB_USER", "postgres"),
            "PASSWORD": os.environ.get("DB_PASSWORD", "postgres"),
            "HOST": os.environ.get("DB_HOST", "localhost"),
            "PORT": os.environ.get("DB_PORT", "5432"),
        }
    }


# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "UserAttributeSimilarityValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "MinimumLengthValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "CommonPasswordValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "NumericPasswordValidator"
        ),
    },
]


# Internationalization
LANGUAGE_CODE = "en-us"
TIME_ZONE = "Asia/Kolkata"
USE_I18N = True
USE_TZ = True


# Static files
STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"

STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": (
            "whitenoise.storage.CompressedManifestStaticFilesStorage"
        ),
    },
}


# Uploaded files
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"


# Email
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"


WHITENOISE_MANIFEST_STRICT = False


# CSRF trusted origins: defaults support Render domains and custom domain omsreminders.com
CSRF_TRUSTED_ORIGINS_ENV = os.environ.get("CSRF_TRUSTED_ORIGINS")
if CSRF_TRUSTED_ORIGINS_ENV:
    CSRF_TRUSTED_ORIGINS = [
        origin.strip()
        for origin in CSRF_TRUSTED_ORIGINS_ENV.split(",")
        if origin.strip()
    ]
else:
    CSRF_TRUSTED_ORIGINS = [
        "https://*.onrender.com",
        "https://omsreminders.com",
        "https://www.omsreminders.com",
        "http://localhost:8000",
        "http://127.0.0.1:8000",
        "http://localhost",
        "http://127.0.0.1",
    ]


DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"