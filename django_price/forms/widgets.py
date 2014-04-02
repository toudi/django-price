from django import forms
from django.core.exceptions import ObjectDoesNotExist

__all__ = ('InputPriceWidget',)

class NotRequiredCheckboxInput(forms.CheckboxInput):
    def build_attrs(self, extra_attrs=None, **kwargs):
        attrs = super(NotRequiredCheckboxInput, self).build_attrs(extra_attrs, **kwargs)
        if 'required' in attrs:
            del attrs['required']
        return attrs

class InputMoneyPriceWidget(forms.MultiWidget):
    
    def __init__(self, fields, *args, **kwargs):
        widgets = [f.widget for f in fields]
        widgets[2] = NotRequiredCheckboxInput()

        super(InputMoneyPriceWidget, self).__init__(widgets, *args, **kwargs)

    def decompress(self, value):
        if value:
            try:
                v = value.instance()
                return [v.value.amount, v.value.currency, v.is_gross, v.tax.pk]
            except ObjectDoesNotExist:
                pass
        return [None, None, None, None]
