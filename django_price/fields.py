from django.db.models import fields
from django.db.models import ForeignKey
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser
from decimal import Decimal


tax_field_name = lambda name: '%s_tax' % name
gross_field_name = lambda name: '%s_gross' % name
is_gross_name = lambda name: '%s_is_gross' % name


class Price(object):
    def __init__(self, value=0, is_gross=False, tax=0):
        try:
            self.value = Decimal(value)
        except:
            pass

        self.is_gross = is_gross
        self.tax = Decimal(tax)
        if self.tax > 1:
            self.tax/=100

    def netto(self):
        if not self.is_gross:
            return self.value

        return self.value / (1 + self.tax)

    def gross(self):
        if self.is_gross:
            return self.value

        return self.value * (1 + self.tax)

    def tax_value(self):
        return self.value * self.tax


class PriceFieldProxy(object):
    def __init__(self, field):
        self.field = field
        self.netto_field = field.name
        self.gross_field_name = gross_field_name(field.name)
        self.tax_field_name = tax_field_name(field.name)
        self.is_gross_name = is_gross_name(field.name)

    def _price_from_obj(self, obj):
        return Price(
            obj.__dict__[self.netto_field],
            obj.__dict__[self.is_gross_name],
            obj.__dict__[self.tax_field_name]
        )

    def __get__(self, obj, type=None):
        if obj is None:
            raise AttributeError('Can only be accessed via an instance.')
        if not isinstance(obj.__dict__[self.field.name], Price):
            obj.__dict__[self.field.name] = self._price_from_obj(obj)
        return obj.__dict__[self.field.name]

    def __set__(self, obj, value):
        if isinstance(value, Price):
            obj.__dict__[self.field.name] = value.netto
            obj.__dict__[self.is_gross_name] = value.is_gross
            obj.__dict__[self.tax_field_name] = value.tax
            obj.__dict__[self.gross_field_name] = value.gross

class PriceField(fields.DecimalField):
    def __init__(self, **kwargs):
        self.frozen_by_south = kwargs.pop('frozen_by_south', None)
        self.money_kwargs    = kwargs.pop('money_kwargs', {})
        super(PriceField, self).__init__(**kwargs)

    def contribute_to_class(self, cls, name):
        netto_field_name = name
        netto_field_class_name = getattr(settings, 'AMOUNT_MONEY_CLASS', 'django.db.models.fields.DecimalField')
        imp = netto_field_class_name.split('.')
        netto_field_class = getattr(__import__('.'.join(imp[:-1]), locals(), globals(), imp[-1]), imp[-1])
        netto_field = netto_field_class(**self.money_kwargs)
        netto_field.creation_counter = self.creation_counter

        _is_gross_name = is_gross_name(name)
        _is_gross = fields.BooleanField(default=False)
        _is_gross.creation_counter = self.creation_counter

        _gross_field_name = gross_field_name(name)
        _gross_field = netto_field_class(**self.money_kwargs)
        _gross_field.creation_counter = self.creation_counter

        t_field_name = tax_field_name(name)
        t_field      = ForeignKey(getattr(settings, 'AMOUNT_TAX_CLASS', 'django_price.Tax'))
        t_field.creation_counter = self.creation_counter

        # super(PriceField, self).contribute_to_class(cls, name)

        cls.add_to_class(netto_field_name, netto_field)
        cls.add_to_class(_is_gross_name, _is_gross)
        cls.add_to_class(_gross_field_name, _gross_field)
        cls.add_to_class(t_field_name, t_field)

        
        setattr(cls, name, PriceFieldProxy(self))
