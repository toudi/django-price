from django.db import models


class AbstractTax(models.Model):
    description = models.CharField(max_length=32)
    value = models.DecimalField(max_digits=5, decimal_places=4)

    class Meta:
        abstract = True


class Tax(AbstractTax):
    # pass

    class Meta:
        app_label = 'django_price'
