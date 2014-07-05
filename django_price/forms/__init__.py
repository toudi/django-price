from fields import *
from django.forms import ModelForm

class MoneyPriceModelForm(ModelForm):
    # TODO: make this more dynamic (different form field name than price)
    price = MoneyPriceFormField()

    def __init__(self, *args, **kwargs):
        if 'instance' in kwargs:
            kwargs.setdefault('initial', {})['price'] = kwargs['instance'].price
        return super(MoneyPriceModelForm, self).__init__(*args, **kwargs)

class DecimalPriceModelForm(ModelForm):
    price = DecimalPriceFormField()

    def __init__(self, *args, **kwargs):
        if 'instance' in kwargs:
            kwargs.setdefault('initial', {})['price'] = kwargs['instance'].price
        return super(DecimalPriceModelForm, self).__init__(*args, **kwargs)
