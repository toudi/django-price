from django import template
from moneyed.localization import format_money

register = template.Library()

@register.filter
def format(value, decimal_places=2):
    # this method is private, but we do need to use it..
    # let's use obj._ClassName__private_method name trick
    if value._MoneyPatched__use_l10n():
        locale = value._MoneyPatched__get_current_locale()
        if locale:
            return format_money(value, locale=locale, decimal_places=decimal_places)

    return format_money(value, decimal_places=decimal_places)