from django.utils.translation import ugettext_lazy as _
from decimal import Decimal
from django import forms
from moneyed import Money
from widgets import InputMoneyPriceWidget
from widgets import InputPriceWidget
from django_price.price import PriceTaxFK
from django_price.models import Tax
from djmoney.forms.fields import MoneyField
from djmoney.forms.widgets import CURRENCY_CHOICES
from django.forms import fields

__all__ = ('MoneyPriceFormField', 'DecimalPriceFormField')

class MoneyPriceFormField(forms.MultiValueField):
    def __init__(self, *args, **kwargs):
        price_field = forms.DecimalField()
        currency_field = forms.ChoiceField(choices=CURRENCY_CHOICES)
        is_gross_field = forms.BooleanField(required=False)
        tax_field = forms.ModelChoiceField(queryset=Tax.objects.all(), required=True)
        fields = (price_field, currency_field, is_gross_field, tax_field)
        self.widget = InputMoneyPriceWidget(fields)
        super(MoneyPriceFormField, self).__init__(fields, *args, **kwargs)

    def compress(self, data_list):
        if data_list[0] is None:
            return None
        return PriceTaxFK(
            value=Money(data_list[0],data_list[1]),
            is_gross=data_list[2],
            tax=data_list[3]
        )

class DecimalPriceFormField(forms.MultiValueField):
    def __init__(self, *args, **kwargs):
        price_field = forms.DecimalField()
        is_gross_field = forms.BooleanField(required=False)
        tax_field = forms.ModelChoiceField(queryset=Tax.objects.all(), required=True)
        fields = (price_field, is_gross_field, tax_field)
        self.widget = InputPriceWidget(fields)
        super(DecimalPriceFormField, self).__init__(fields, *args, **kwargs)

    def compress(self, data_list):
        if data_list[0] is None:
            return None

        return PriceTaxFK(
            value=Decimal(data_list[0]),
            is_gross=data_list[1],
            tax=data_list[2]
        )