from setuptools import setup

setup(
    name='django-price',
    description='Support for storing prices (netto/gross) in django app',
    maintainer='Mateusz Mikołajczyk',
    maintainer_email='mikolajczyk.mateusz@gmail.com',
    url='https://github.com/toudi/django-price',
    packages=(
        'django_price',
        'django_price.models',
        'django_price.models.fields',
        'django_price.forms',
        'django_price.tests',
    ),
    install_requires=(
        'setuptools',
        'django-composite-field',
    )
)
