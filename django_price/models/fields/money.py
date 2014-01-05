from django_price.models.fields.decimal import BasePriceMetaclass
from django_price.price import PriceTaxFK
from composite_field.base import CompositeField
from djmoney.models.fields import MoneyField
from django.db.models import DecimalField
from django.db.models import BooleanField
from django.db.models import ForeignKey
from django.conf import settings


class MoneyPriceField(BasePriceMetaclass, CompositeField):
    def __init__(
        self,
        prefix=None,
        default_currency=None,
        decimal_places=2,
        max_digits=12,
    ):
        self.subfields = {
            'netto': MoneyField(
                max_digits=max_digits, decimal_places=decimal_places,
                default_currency=default_currency,
            ),
            'gross': MoneyField(
                max_digits=max_digits, decimal_places=decimal_places,
                default_currency=default_currency,
            ),
            'is_gross': BooleanField(default=False),
            'tax': DecimalField(
                max_digits=max_digits, decimal_places=decimal_places,
            ),
        }
        self.init()
        super(MoneyPriceField, self).__init__(prefix)


class MoneyPriceFieldTaxForeignKey(MoneyPriceField):
    def init(self):
        self.subfields['tax'] = ForeignKey(settings.PRICE_TAX_MODEL)
        self.price_class = PriceTaxFK
