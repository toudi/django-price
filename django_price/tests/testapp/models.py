from django.db import models
from django_price.models.fields.decimal import DecimalPriceField
from django_price.models.fields.decimal import DecimalPriceFieldTaxForeignKey
from django_price.models.fields.money import MoneyPriceField


class TestModel(models.Model):
    price = DecimalPriceField()


class TestModelTaxForeignKey(models.Model):
    price = DecimalPriceFieldTaxForeignKey()


class TestModelMoney(models.Model):
    price = MoneyPriceField(default_currency='USD')
