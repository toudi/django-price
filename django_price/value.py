class Value(object):
    def __init__(self, price, quantity):
        self.price = price
        self.quantity = quantity

    def gross_value(self):
        return self.quantity * self.price.gross

    def netto_value(self):
        return self.quantity * self.price.netto

    def tax_value(self):
        return self.quantity * self.price.tax_value()

    def __repr__(self):
        return 'Value(quantity=%r,price=%r)' % (self.quantity, self.price)