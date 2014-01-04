from decimal import Decimal


class Price(object):
    def __init__(self, value=0, is_gross=False, tax=0):
        self._tax = None
        self._value = None
        self.value = value
        self.is_gross = is_gross
        self.tax = tax
        if self.tax > 1:
            self.tax /= 100

    def set_tax(self, value):
        self._tax = Decimal(value)

    def get_tax(self):
        return self._tax

    def set_value(self, value):
        try:
            self._value = Decimal(value)
        except TypeError:
            self._value = value

    def get_value(self):
        return self._value

    tax = property(get_tax, set_tax)
    value = property(get_value, set_value)

    def get_netto(self):
        if not self.is_gross:
            return self.value

        return self.value - self.tax_value()

    def set_netto(self, value):
        self.value = value
        self.is_gross = False

    netto = property(get_netto, set_netto)

    def get_gross(self):
        if self.is_gross:
            return self.value

        return self.value + self.tax_value()

    def set_gross(self, value):
        self.value = value
        self.is_gross = True

    gross = property(get_gross, set_gross)

    def tax_value(self):
        return self.value * self.tax

    def __repr__(self):
        return 'Price(netto=%r,gross=%r,tax=%r,tax_value=%r,is_gross=%r)' % (
            self.netto,
            self.gross,
            self.tax,
            self.tax_value(),
            self.is_gross
        )
