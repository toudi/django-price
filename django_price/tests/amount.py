"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from .. import Amount
from decimal import Decimal
from random import random


class AmountTest(TestCase):
    def test_gross_value(self):
    	gross_value = random()

    	gross_amount = Amount(gross_value, 0, True)

    	self.assertEquals(gross_amount.gross(), gross_value)

    	net_worth_value = Decimal(random())
    	tax_value = Decimal(random())

    	gross_amount = Amount(net_worth_value, tax_value)
    	self.assertEquals(gross_amount.gross(), Decimal(net_worth_value * (1+tax_value)))

    def test_addition(self):
    	net_worth_value = Amount(random())
    	expectedDifference = random()

    	diff = net_worth_value + expectedDifference
    	self.assertEquals(diff, expectedDifference)