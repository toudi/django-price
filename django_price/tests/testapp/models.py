from django.db import models
from django_price.fields import DecimalPriceField


class TestModel(models.Model):
    price = DecimalPriceField()
