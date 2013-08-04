The basic idea behind this field is that it allows for easy storing price values:

netto, tax, gross.

the default storage of amount is decimal field, but you can specify your own via settings.

# Usage

This field registers itself as a completely new, fake field on the model. If you want to save the price to the model, you should use the Price class and define a PriceField inside your model. Here's how:

```
from django.db import models
from django_price.fields import PriceField

# Create your models here.

class Foo(models.Model):
    price = PriceField(decimal_places=2, max_digits=3)
```

That's it!. The above example will use django's DecimalField for price representation.

However, sometimes this is not enough. If you want to use django-money app, you can do so by specifying the amount class in the settings.py file:

```
AMOUNT_MONEY_CLASS = 'djmoney.models.fields.MoneyField'
```

then you need to provide default currency to your price. Otherwise, django-money won't accept this:

```
from django.db import models
from django_price.fields import PriceField

# Create your models here.

class Foo(models.Model):
    price = PriceField(decimal_places=2, max_digits=3, default_currency='USD')
```

# Forms support

PriceField supports django forms. If you want to display the form field, just use price field. Here's how:

```
from django import forms
from apps.foo.models import Foo

class F(forms.ModelForm):
    class Meta:
        model = Foo
        fields = ('price',)
```

PriceField will always render the most significant price to edit. For example, if you have set the price to be netto, the netto value will be displayed. But if you select 'is_gross' checkbox, the gross value will be used as a base for editing.

I hope you enjoy this field as much as i enjoyed writing it ;)
