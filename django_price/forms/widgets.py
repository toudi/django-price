from django import forms
from moneyed import Money, CURRENCIES, DEFAULT_CURRENCY_CODE
from decimal import Decimal
import operator
from djmoney.forms.widgets import InputMoneyWidget
from django_price import Price

__all__ = ('InputPriceWidget',)

class InputPriceWidget(forms.TextInput):
    
    def __init__(self, attrs=None):
        self.value_widget = InputMoneyWidget(attrs={})
        self.is_gross_widget = forms.CheckboxInput()
        self.tax_input = forms.TextInput()
        super(InputPriceWidget, self).__init__(attrs)
    
    def render(self, name, value, attrs=None):
        _value = ''
        is_gross = False
        tax = 0
        if isinstance(value, Price):
            _value = value.netto()
            tax = value.tax
            is_gross = value.is_gross
            # we always need to show the most important field.
            # if the price includes tax, let's show this. If not,
            # we'll stick to the netto
            if value.is_gross:
                _value = value.gross()
        if isinstance(value, tuple):
            _value = value[0]
        if isinstance(value, int) or isinstance(value, Decimal):
            amount = value
        result = self.value_widget.render(name, _value, attrs={})
        result += self.is_gross_widget.render(name+'_is_gross', is_gross)
        result += self.tax_input.render(name+'_tax', tax)
        return result
    
    def value_from_datadict(self, data, files, name):
        is_gross = data.get(name+'_is_gross', False)
        if is_gross == 'on':
            is_gross = True
        return (
            data.get(name, None),
            data.get(name+'_currency', None),
            is_gross,
            data.get(name+'_tax', None),
        )