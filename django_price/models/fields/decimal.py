from django.db.models import fields
from django.conf import settings
from django_price.price import PriceObject
from django_price.price import Price
from django_price.price import PriceTaxFK
from composite_field.base import CompositeField
from composite_field.base import CompositeFieldBase
from django.db.models import DecimalField
from django.db.models import BooleanField
from django.db.models import ForeignKey


class PriceProxy(CompositeField.Proxy):
    def _set(self, value):
        if not isinstance(value, PriceObject):
            raise Exception('Cannot assign value which is not a price!')

        return super(PriceProxy, self)._set(value)

    def get_value(self):
        value = self.netto
        if self.is_gross:
            value = self.gross

        return self._composite_field.price_class(
            value=value,
            tax=self.tax,
            is_gross=self.is_gross
        )


class BasePriceMetaclass(object):
    def init(self):
        self.price_class = Price

    def get_proxy(self, model):
        return PriceProxy(self, model)


class DecimalPriceField(BasePriceMetaclass, CompositeField):
    def __init__(self, prefix=None, decimal_places=2, max_digits=12):
        self.subfields = {
            'netto': DecimalField(
                max_digits=max_digits, decimal_places=decimal_places,
                default=0
            ),
            'gross': DecimalField(
                max_digits=max_digits, decimal_places=decimal_places,
                default=0
            ),
            'is_gross': BooleanField(default=False),
            'tax': DecimalField(
                max_digits=max_digits, decimal_places=decimal_places,
                default=0),
        }
        self.init()
        super(DecimalPriceField, self).__init__(prefix)


class DecimalPriceFieldTaxForeignKey(DecimalPriceField):
    def init(self):
        self.subfields['tax'] = ForeignKey(settings.PRICE_TAX_MODEL)
        self.price_class = PriceTaxFK
