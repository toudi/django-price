from decimal import Decimal
from django.test import TestCase
from django_price.tests.testapp.models import TestModel
from django_price.tests.testapp.models import TestModelMoney
from django_price.tests.testapp.models import TestModelTaxForeignKey
from django_price.models.tax import Tax
from moneyed import Money
from django_price.price import Price
from django_price.price import PriceTaxFK
from django_price.price import PriceObject
from django.db.models import F


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
        self.assertIsInstance(model.price.get_value(), PriceObject)
        self.assertEquals(model.price.get_value().netto, Decimal(15))

    def test_that_relative_update_works(self):
        price = Price(10)
        model = TestModel(price=price)
        model.save()
        model.price_netto = F('price_netto') + 10
        model.save()
        model = TestModel.objects.get(pk=model.pk)
        self.assertEquals(model.price.netto, Decimal(20))


class MoneyTestCase(TestCase):
    def test_can_pass_money_instance(self):
        amount = Money(10, 'USD')
        price = Price(amount)
        model = TestModelMoney(price=price)
        self.assertEquals(model.price_netto_currency, unicode(amount.currency))
        self.assertIsInstance(model.price.get_value().netto, Money)


class TaxAsForeignKeyTestCase(TestCase):
    def test_that_tax_field_is_a_foreign_key(self):
        tax = Tax.objects.create(
            description='test tax', value=Decimal('0.22')
        )

        price = PriceTaxFK(100, tax=tax)

        model = TestModelTaxForeignKey(
            price=price
        )

        self.assertEquals(122, model.price.gross)
        self.assertIsInstance(model.price.get_value(), PriceTaxFK)
        self.assertEquals(tax.pk, model.price_tax_id)
