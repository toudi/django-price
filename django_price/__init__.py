from decimal import Decimal

class Amount(object):
	def __init__(self, value, tax=0, is_gross=False):
		"""
		Creates the Amount instance.

		value is the actual amount (either netto or gross)
		tax is a decimal object with taxation value.
		is_gross specifies whether the value already contains the tax or not.
		"""
		self._value    = Decimal(value)
		self._tax      = 1 + Decimal(tax)
		self._is_gross = is_gross

	def net_worth(self):
		if self._is_gross:
			return self._value / self._tax
		return self._value

	def gross(self):
		if self._is_gross:
			return self._value

		return self._value * self._tax

	def tax_amount(self):
		if self._is_gross:
			return self._value - self.net_worth()

		return self._value * self._tax
