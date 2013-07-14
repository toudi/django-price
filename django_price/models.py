from django.db import models

class Tax(models.Model):
	description = models.CharField(max_length=32)
	value = models.DecimalField(max_digits=5, decimal_places=4)