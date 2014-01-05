DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    },
}

INSTALLED_APPS = (
    'django_price',
    'django_price.tests.testapp',
)


SECRET_KEY = 'abcde12345'
PRICE_TAX_MODEL = 'django_price.Tax'
