from django.db.models import fields
from django.conf import settings
from django_price.price import Price
from composite_field.base import CompositeField
from composite_field.base import CompositeFieldBase
from django.db.models import DecimalField
from django.db.models import BooleanField


tax_field_name = lambda name: '%s_tax' % name
netto_field_name = lambda name: '%s_netto' % name
gross_field_name = lambda name: '%s_gross' % name
is_gross_name = lambda name: '%s_is_gross' % name
field_currency = lambda name: '%s_currency' % name


class PriceProxy(CompositeField.Proxy):
    def _set(self, value):
        if not isinstance(value, Price):
            raise Exception('Cannot assign value which is not a price!')

        return super(PriceProxy, self)._set(value)


class BasePriceMetaclass(object):
    def get_proxy(self, model):
        return PriceProxy(self, model)


class DecimalPriceField(BasePriceMetaclass, CompositeField):
    def __init__(self, prefix=None, decimal_places=2, max_digits=12):
        self.subfields = {
            'netto': DecimalField(
                max_digits=max_digits, decimal_places=decimal_places),
            'gross': DecimalField(
                max_digits=max_digits, decimal_places=decimal_places),
            'is_gross': BooleanField(default=False),
            'tax': DecimalField(
                max_digits=max_digits, decimal_places=decimal_places),
        }
        super(DecimalPriceField, self).__init__(prefix)

# class PriceFieldProxy(object):
#     def __init__(self, field):
#         self.field = field
#         self.netto_field_name = netto_field_name(field.name)
#         self.gross_field_name = gross_field_name(field.name)
#         self.tax_field_name = tax_field_name(field.name)
#         self.is_gross_name = is_gross_name(field.name)

#     def _price_from_obj(self, obj):
#         vfield = self.netto_field_name
#         if obj.__dict__[self.is_gross_name]:
#             vfield = self.gross_field_name
#         return Price(
#             getattr(obj, vfield), #because of getattr we can get django-money instance with the currency.
#             obj.__dict__[self.is_gross_name],
#             obj.__dict__[self.tax_field_name] or 0
#         )

#     def __get__(self, obj, type=None):
#         if obj is None:
#             raise AttributeError('Can only be accessed via an instance.')
#         if not self.field.name in obj.__dict__:
#             obj.__dict__[self.field.name] = self._price_from_obj(obj)
#         return obj.__dict__[self.field.name]

#     def __set__(self, obj, value):
#         if isinstance(value, Price):
#             obj.__dict__[self.netto_field_name] = value.netto()
#             try:
#                 setattr(obj, field_currency(self.netto_field_name), value.netto().currency)
#             except:
#                 pass
#             try:
#                 setattr(obj, field_currency(self.gross_field_name), value.gross().currency)
#             except:
#                 pass
#             obj.__dict__[self.is_gross_name] = value.is_gross
#             obj.__dict__[self.tax_field_name] = value.tax
#             obj.__dict__[self.gross_field_name] = value.gross()
#             # this is needed so that django picks up 'fresh' value in __get__ method.
#             del(obj.__dict__[self.field.name])

# class PriceField(fields.Field):
#     def __init__(self, **kwargs):
#         self.frozen_by_south = kwargs.pop('frozen_by_south', None)
#         self.money_kwargs    = kwargs
#         super(PriceField, self).__init__()

#     def contribute_to_class(self, cls, name):
#         _netto_field_name = netto_field_name(name)
#         netto_field_class_name = getattr(settings, 'AMOUNT_MONEY_CLASS', 'django.db.models.fields.DecimalField')
#         imp = netto_field_class_name.split('.')
#         netto_field_class = getattr(__import__('.'.join(imp[:-1]), locals(), globals(), imp[-1]), imp[-1])
#         netto_field = netto_field_class(**self.money_kwargs)
#         netto_field.creation_counter = self.creation_counter

#         _is_gross_name = is_gross_name(name)
#         _is_gross = fields.BooleanField(default=False)
#         _is_gross.creation_counter = self.creation_counter

#         _gross_field_name = gross_field_name(name)
#         _gross_field = netto_field_class(**self.money_kwargs)
#         _gross_field.creation_counter = self.creation_counter

#         t_field_name = tax_field_name(name)
#         t_field      = fields.DecimalField(max_digits=6, decimal_places=4)
#         t_field.creation_counter = self.creation_counter

#         #cls._meta.add_field(self)
#         self.attname = name
#         self.name = name
#         """the whole purpose of this line is to make django think that
#         this is a legitimate field (in terms of forms.ModelForm).
#         Django won't let you use a field which cannot be bound to database column.
#         We therefore set this to netto field name.
#         This **is** important - please refer to get_db_prep_save
#         """
#         self.db_column = netto_field_name(name)
#         super(PriceField, self).contribute_to_class(cls, name)

#         cls.add_to_class(_netto_field_name, netto_field)
#         cls.add_to_class(_is_gross_name, _is_gross)
#         cls.add_to_class(_gross_field_name, _gross_field)
#         cls.add_to_class(t_field_name, t_field)

#         setattr(cls, name, PriceFieldProxy(self))

#     def get_db_prep_save(self, value, **kwargs):
#         """This is actually very important method for this field.
#         Django tries to save instances of the fields to the database.
#         Well, PriceField is completely fake field, so we cannot just save it.
#         Therefore we return just the netto value.
#         Note: This is important, because we have set the db_column to netto column
#         This saves us the dirty work of monkey-patching the managers in order to
#         extract all of Price values
#         """
#         try:
#             return value.netto().amount
#         except:
#             return value.netto()


#     def formfield(self, **kwargs):
#         defaults = {'form_class': forms.PriceField}
#         defaults.update(kwargs)
#         return super(PriceField, self).formfield(**defaults)
