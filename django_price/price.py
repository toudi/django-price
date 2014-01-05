from decimal import Decimal


class PriceObject(object):
    pass


class Price(PriceObject):
    def __init__(self, value=0, is_gross=False, tax=0):
        self._tax = None
        self._value = None
        self.value = value
        self.is_gross = is_gross
        self.tax = tax

    def set_tax(self, value):
        if type(value) == float:
            value = str(value)
        self._tax = Decimal(value)
        if self._tax > 1:
            self._tax /= 100

    def get_tax(self):
        return self._tax

    def __get_tax(self):
        """this method should always return the value of a tax
        """
        tax = self._tax
        if hasattr(tax, 'pk'):
            tax = tax.value
        return tax

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
        tax = self.__get_tax()

        value = self.value * tax

        if self.is_gross:
            value /= (1 + tax)

        return value

    def __repr__(self):
        return 'Price(netto=%r,gross=%r,tax=%r,tax_value=%r,is_gross=%r)' % (
            self.netto,
            self.gross,
            self.tax,
            self.tax_value(),
            self.is_gross
        )


class PriceTaxFK(Price):
    def set_tax(self, value):
        self._tax = value

    def get_tax(self):
        return self._tax

    tax = property(get_tax, set_tax)
