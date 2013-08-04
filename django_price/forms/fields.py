from django.utils.translation import ugettext_lazy as _
from django import forms
from widgets import InputPriceWidget
from django_price import Price

__all__ = ('PriceField',)

class PriceField(forms.DecimalField):
    
    def __init__(self, *args, **kwargs):
        self.widget = InputPriceWidget()
        super(PriceField, self).__init__(*args, **kwargs)
    
    def to_python(self, value):
        if not isinstance(value, tuple):
            raise Exception("Invalid money input, expected sum and currency.")

        price = super(PriceField, self).to_python(value[0])
        # i don't quite like this part of code, but currently don't know how to do it better.
        # the idea is, if the value tuple is long enough, i assume that this is Money instance
        # (With the currency). Otherwise - i assume regular decimal field
        if len(value) > 3 and value[1] is not None:
            from moneyed import Money
            price = Money(amount=value[0], currency=value[1])
        is_gross = value[2]
        tax = value[-1]
        # the order of those fields can be extracted from widgets.py file (method value_from_datadict)
        if not tax:
            raise forms.ValidationError(_(u'Tax is missing'))
        out = Price(value=price, tax=tax, is_gross=is_gross)
        return Price(value=price, tax=tax, is_gross=is_gross)
    
    def validate(self, value):
        if not isinstance(value, Price):
            raise Exception("Invalid money input, expected Money object to validate.")
        
        try:
            super(PriceField, self).validate(value._value.amount)
        except:
            super(PriceField, self).validate(value._value)
