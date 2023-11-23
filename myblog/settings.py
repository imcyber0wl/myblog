from pathlib import Path
#import .logging_dict
import dj_database_url

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-9zq0wopill4v^aenp2i)7+x6+#)45zwoo*epux^9s6kvg#^wsl'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'blog',
    'bootstrap5',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

ROOT_URLCONF = 'myblog.urls'

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

WSGI_APPLICATION = 'myblog.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'postgres',
        'USER': 'postgres',
        'PASSWORD': 'admin1234',
        'HOST': 'database-1.cyiaaizn3jxj.eu-north-1.rds.amazonaws.com',
        'PORT': '5432',
    }}

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'

MEDIA_ROOT="media/"
MEDIA_URL="https://myblogbucketme.s3.amazonaws.com/"#"/media/"

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.db.DatabaseCache",
        "LOCATION": "my_cache_table",
    }
}


FORMATTERS = (
    {
 "verbose": {
     "format": "{levelname} {asctime:s} {threadName} {thread:d} {module} {filename} {lineno:d} {name} {funcName} {process:d} {message}",
      "style": "{",
  },
       
 "simple": {
 "format": "{levelname} {asctime:s} {module} {filename} {lineno:d} {funcName} {message}",
   "style": "{",
        },
    },
)



HANDLERS = {
"console_handler": {
        "class": "logging.StreamHandler", #use console
        "formatter": "simple",
    },

}

LOGGERS={
"django": {
"handlers":["console_handler"],
"level":"INFO",
"propagate":False,
},

}


LOGGING= {
"version" :1,
"disable_existing_loggers":False,
"formatters":FORMATTERS[0],
"handlers":HANDLERS,
"loggers":LOGGERS,
}


AWS_ACCESS_KEY_ID = 'AKIAV774QTBE2NQDMIO6 '       
AWS_SECRET_ACCESS_KEY = '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'
AWS_STORAGE_BUCKET_NAME = 'myblogbucketme' #put bucket name here
AWS_S3_SIGNATURE_NAME = 's3v4',
AWS_S3_REGION_NAME = 'eu-north-1' #write region here like us-east-1
AWS_S3_FILE_OVERWRITE = False
AWS_DEFAULT_ACL =  None
AWS_S3_VERITY = True
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'


