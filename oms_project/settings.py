import os
from pathlib import Path

import dj_database_url


BASE_DIR = Path(__file__).resolve().parent.parent

# Load local .env file if present
env_file = BASE_DIR / ".env"
if env_file.exists():
    try:
        with open(env_file, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, val = line.split("=", 1)
                    os.environ.setdefault(key.strip(), val.strip().strip('"').strip("'"))
    except Exception:
        pass


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


# Database Configuration
DEFAULT_DATABASE_URL = "postgresql://neondb_owner:npg_9t5RjvHVesWU@ep-tiny-sound-b571duzk-pooler.c-7.us-east-2.aws.neon.tech/neondb?sslmode=require"
DATABASE_URL = os.environ.get("DATABASE_URL") or DEFAULT_DATABASE_URL
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
    # Hosted PostgreSQL (Neon, Render PostgreSQL, Supabase, etc.)
    is_internal = any(k in DATABASE_URL for k in ["localhost", "127.0.0.1", "dpg-", ".internal"])
    ssl_require = False if is_internal else (os.environ.get("DB_SSL_REQUIRE", "true").lower() in ("true", "1", "yes"))
    conn_max_age = 0 if "-pooler" in DATABASE_URL else 600
    DATABASES = {
        "default": dj_database_url.parse(
            DATABASE_URL,
            conn_max_age=conn_max_age,
            ssl_require=ssl_require,
        )
    }

else:
    # Fallback SQLite
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
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

# Console logging for cloud host observability (Render logs)
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "simple": {
            "format": "[%(asctime)s] %(levelname)s %(name)s: %(message)s"
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "simple",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "INFO",
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": True,
        },
        "django.request": {
            "handlers": ["console"],
            "level": "ERROR",
            "propagate": False,
        },
    },
}