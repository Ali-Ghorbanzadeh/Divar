from pathlib import Path
from decouple import config

BASE_DIR = Path(__file__).resolve().parent.parent



SECRET_KEY = config("SECRET_KEY", default="&(dj-development-secret_key)$")

DEBUG = config("DEBUG", cast=bool, default=True)

ALLOWED_HOSTS = ["*"] if DEBUG else config("ALLOWED_HOSTS", cast=lambda hosts: hosts.split(','))
APPLICATIONS = ['core', 'advertisement', 'accounts']
DEFAULT_FROM_EMAIL = config("EMAIL_DEFAULT_FROM", default="noreply@development.dev")
INSTALLED_APPS = [

    'jazzmin',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third-party applications:
    "rest_framework",
    'drf_spectacular',

    # Applications:
    *list(map(lambda app: f"apps.{app}", APPLICATIONS)),
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'apps.advertisement.middleware.VisitAdvertisementMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'config.wsgi.application'


AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


LANGUAGE_CODE = 'en-us'
TIME_ZONE = config("TIME_ZONE", default="Asia/Tehran")

USE_I18N = True

USE_TZ = False


STATIC_URL = 'static/'
STATIC_ROOT_PATH = BASE_DIR / "storage/static"

if DEBUG:
    # Static
    STATICFILES_DIRS = [
        STATIC_ROOT_PATH,
    ]

    # Email
    EMAIL_HOST = "localhost"
    EMAIL_PORT = 2525
    EMAIL_HOST_USER = ""
    EMAIL_HOST_PASSWORD = ""
    EMAIL_USE_TLS = False

    # Database
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': config("DB_NAME"),
            'USER': config("DB_USER"),
            'PASSWORD': config("DB_PASSWORD"),
            'PORT': config("DB_PORT"),
            'HOST': config("DB_HOST"),
        }
    }

    # Cache
    CACHES = {
        "default": {
            "BACKEND": "django.core.cache.backends.redis.RedisCache",
            "LOCATION": "redis://localhost:6379/0",
        }
    }

    CORS_ALLOW_ALL_ORIGINS = True
else:
    # Statics
    STATIC_ROOT = STATIC_ROOT_PATH

    # Email
    EMAIL_HOST = config("EMAIL_HOST")
    EMAIL_PORT = config("EMAIL_PORT", cast=int)
    EMAIL_HOST_USER = config("EMAIL_HOST_USER")
    EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD")
    EMAIL_USE_TLS = config("EMAIL_USE_TLS", cast=bool)

    # Database
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': config("DB_NAME"),
            'USER': config("DB_USER"),
            'PASSWORD': config("DB_PASSWORD"),
            'PORT': config("DB_PORT"),
            'HOST': config("DB_HOST"),
        }
    }

    # Cache
    REDIS_URL = config("REDIS_URL")
    CACHES = {
        "default": {
            "BACKEND": "django.core.cache.backends.redis.RedisCache",
            "LOCATION": REDIS_URL,
        }
    }

    # # Security params:
    # SECURE_HSTS_SECONDS = 12 * 30 * 24 * 60 * 60
    # SECURE_HSTS_PRELOAD = True
    # SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    # SECURE_SSL_REDIRECT = True
    # SECURE_PROXY_SSL_HEADER = "HTTP_X_FORWARDED_PROTO" ,"https"
    # USE_X_FORWARDED_HOST = True
    # SESSION_COOKIE_SECURE = True
    # CSRF_COOKIE_SECURE = True
    # SECURE_REFERRER_POLICY = "strict-origin"
    # X_FRAME_OPTIONS = "SAMEORIGIN"
    # SESSION_COOKIE_AGE = 3 * 60 * 60
    # SESSION_TIMEOUT = 24 * 60 * 60

    # CORS params
    # CORS_ALLOW_ALL_ORIGINS = False
    # CORS_ALLOWED_ORIGINS = config(
    #     "ALLOWED_HOSTS",
    #     cast=lambda hosts: hosts.split(','),
    #     default="http://0.0.0.0:8000, http://localhost:8000"
    # )


MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'storage/media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'accounts.UserProfile'

REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

JAZZMIN_SETTINGS = {
    "site_title": "Divar",
    "site_header": "Divar",
    "site_brand": "Divar",
    "login_logo": None,
    "login_logo_dark": True,
    "site_logo_classes": "img-circle",
    "site_icon": None,
    "welcome_sign": "Welcome to the Divar",
    "user_avatar": None,
    # "topmenu_links": [
    #     {"name": "Home",  "url": "admin:index", "permissions": ["AUTH_USER_MODEL"]},
    #     {"name": "Profile", "url": "profile", "new_window": True},
    #     {"app": "accounts"},
    # ],
    # "usermenu_links": [
    #     {"name": "Profile", "url": "profile"},
    #     {"name": "Settings", "url": "settings"},
    # ],
    "show_sidebar": True,
    "navigation_expanded": True,
    "hide_apps": [],
    "hide_models": [],
    "order_with_respect_to": ["auth"],
    "icons": {
        "auth": "fas fa-users-cog",
        "AUTH_USER_MODEL": "fas fa-user",
        "auth.Group": "fas fa-users",
    },
    "default_icon_parents": "fas fa-chevron-circle-right",
    "default_icon_children": "fas fa-circle",
    "related_modal_active": False,
    "custom_css": None,
    "custom_js": None,
    "use_google_fonts_cdn": True,
    "show_ui_builder": True,
    "changeform_format": "vertical_tabs",
    "changeform_format_overrides": {"AUTH_USER_MODEL": "collapsible", "auth.group": "vertical_tabs"},
}

SPECTACULAR_SETTINGS = {
    'TITLE': 'Divar',
    'DESCRIPTION': 'Search and find!',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
}


JAZZMIN_UI_TWEAKS = {
    "navbar_small_text": False,
    "footer_small_text": False,
    "body_small_text": False,
    "brand_small_text": False,
    "brand_colour": "navbar-orange",
    "accent": "accent-warning",
    "navbar": "navbar-dark",
    "no_navbar_border": False,
    "navbar_fixed": False,
    "layout_boxed": False,
    "footer_fixed": False,
    "sidebar_fixed": True,
    "sidebar": "sidebar-dark-warning",
    "sidebar_nav_small_text": False,
    "sidebar_disable_expand": False,
    "sidebar_nav_child_indent": False,
    "sidebar_nav_compact_style": False,
    "sidebar_nav_legacy_style": False,
    "sidebar_nav_flat_style": False,
    "theme": "cerulean",
    "dark_mode_theme": "darkly",
    "button_classes": {
        "primary": "btn-primary",
        "secondary": "btn-secondary",
        "info": "btn-outline-info",
        "warning": "btn-warning",
        "danger": "btn-danger",
        "success": "btn-outline-success"
    },
    "actions_sticky_top": False
}

# Celery

CELERY_BROKER_URL = 'redis://localhost:6379/15'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/15'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Asia/Tehran'
CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True