from decimal import Decimal
from django.test import TestCase
from django_price.tests.testapp.models import TestModel
from django_price.price import Price


class ModelTestCase(TestCase):
    def test_model_has_desired_columns(self):
        model = TestModel()
        self.assertIn('price_netto', model.__dict__)
        field = model._meta.get_field('price_netto')
        self.assertEquals(12, field.max_digits)
        self.assertEquals(2, field.decimal_places)

    def test_assigning_values_to_the_model(self):
        price = Price(10)
        model = TestModel(price=price)
        self.assertEquals(model.price_netto, price.netto)
        # no tax therefore the prices must be equal
        self.assertEquals(model.price_gross, price.netto)
        # no tax therefore tax_value must be equal to 0
        self.assertEquals(Decimal(0), price.tax_value())

        # assert that getting by column name also works
        self.assertEquals(price.netto, model.price.netto)

        # now, let's create a model, but let's only assign one value.
        model = TestModel(price_netto=Decimal(15))
        self.assertIsInstance(model.price.get_value(), Price)
        self.assertEquals(model.price.get_value().netto, Decimal(15))
